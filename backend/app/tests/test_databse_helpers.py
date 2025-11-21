from sqlalchemy.orm import Session
from database import (
    Topic, Question, User, Attempt,
    create_user,
    list_topics,
    record_attempt,
    list_attempts_for_user,
    get_user_accuracy,
)
from tests.conftest import TestingSessionLocal

def test_list_topics_returns_inserted_topics(setup_database):
    db: Session = TestingSessionLocal()
    try:
        topic = Topic(name="Controls", slug="controls")
        db.add(topic)
        db.commit()

        topics = list_topics(db)
        assert len(topics) == 1
        assert topics[0].name == "Controls"
    finally:
        db.close()


def test_attempts_and_accuracy(setup_database):
    db: Session = TestingSessionLocal()
    try:
        user = create_user(db, username="u", email="e@example.com", password_hash="h", google_id=None)
        q = Question(topic_id=1, text="Q?", difficulty=1, solution="a")
        db.add(q)
        db.commit()
        db.refresh(q)

        record_attempt(db, user_id=user.id, question_id=q.id, user_answer="a", correct=True)
        record_attempt(db, user_id=user.id, question_id=q.id, user_answer="b", correct=False)

        attempts = list_attempts_for_user(db, user_id=user.id, limit=10)
        assert len(attempts) == 2
        # should be ordered newest first by submitted_at
        assert attempts[0].submitted_at >= attempts[1].submitted_at

        accuracy = get_user_accuracy(db, user_id=user.id)
        assert accuracy == 0.5
    finally:
        db.close()