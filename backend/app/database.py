import os
from sqlalchemy import create_engine, select, String, Integer, SmallInteger, Text, ForeignKey
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
