from ast import stmt
import datetime
import os
from sqlalchemy import DateTime, create_engine, func, select, String, Integer, SmallInteger, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session, Mapped, mapped_column, relationship
from typing import Sequence

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://wingman:1MegaNemus@wingman-pg-dev.postgres.database.azure.com:5432/wingman?sslmode=require",
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# Models
class Topic(Base):
    __tablename__ = "topics"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # AI suggested adding slug for better URL handling
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    questions: Mapped[list["Question"]] = relationship(back_populates="topic")

class Question(Base):
    __tablename__ = "questions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    solution: Mapped[str] = mapped_column(Text, nullable=False)
    # type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    topic: Mapped["Topic"] = relationship(back_populates="questions")
    attempts: Mapped[list["Attempt"]] = relationship(back_populates="question")

class Attempt(Base):
    __tablename__ = "attempts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)
    user_answer: Mapped[str] = mapped_column(Text, nullable=False)
    correct: Mapped[bool] = mapped_column(nullable=False)

    submitted_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="attempts")
    question: Mapped["Question"] = relationship(back_populates="attempts")


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    google_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    attempts: Mapped[list["Attempt"]] = relationship(back_populates="user")



# Database functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def list_topics(db: Session) -> Sequence[Topic]:
    return db.scalars(select(Topic)).all()

def list_question(db: Session, *, topic_id: int | None = None) -> Sequence[Question]:
    query = select(Question)
    if topic_id is not None:
        query = query.where(Question.topic_id == topic_id)
    return db.scalars(query).all()

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))

def get_user_by_google_id(db: Session, google_id: str) -> User | None:
    return db.scalar(select(User).where(User.google_id == google_id))

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)

def create_user(db: Session, *, username: str, email: str, password_hash: str | None, google_id: str | None) -> User:
    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        google_id=google_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def record_attempt(db: Session, *, user_id: int, question_id: int, user_answer: str, correct: bool) -> Attempt:
    attempt = Attempt(
        user_id=user_id,
        question_id=question_id,
        user_answer=user_answer,
        correct=correct,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt

# we can change the limit later if needed
def list_attempts_for_user(db: Session, *, user_id: int, limit: int = 20) -> Sequence[Attempt]:
        stmt = (
        select(Attempt)
        .where(Attempt.user_id == user_id)
        .order_by(Attempt.submitted_at.desc())
        .limit(limit)
    )
        return db.scalars(stmt).all()

def get_question_by_id(db: Session, question_id: int) -> Question | None:
    return db.get(Question, question_id)

def get_user_accuracy(db: Session, *, user_id: int) -> float:
    total_attempts = db.scalar(
        select(func.count(Attempt.id)).where(Attempt.user_id == user_id)
    )
    if total_attempts == 0:
        return 0.0
    correct_attempts = db.scalar(
        select(func.count(Attempt.id)).where(Attempt.user_id == user_id, Attempt.correct == True)
    )
    return correct_attempts / total_attempts