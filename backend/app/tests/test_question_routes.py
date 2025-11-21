from sqlalchemy.orm import Session
from database import Question

def seed_question(db_session: Session, topic_id: int = 1) -> int:
    q = Question(
        topic_id=topic_id,
        text="What is the chemical formula for water?",
        difficulty=2,
        solution="H2O",
    )
    db_session.add(q)
    db_session.commit()
    db_session.refresh(q)
    return q.id

def test_list_questions_returns_all(client, db_session: Session):
    q_id = seed_question(db_session)

    resp = client.get("/api/questions")
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) == 1
    assert data[0]["id"] == q_id
    assert data[0]["question"] == "What is the chemical formula for water?"
    assert "topic_id" in data[0]
    assert "difficulty" in data[0]

def test_list_questions_filter_by_topic(client, db_session: Session):
    seed_question(db_session, topic_id=1)
    seed_question(db_session, topic_id=2)

    resp = client.get("/api/questions", params={"topic_id": 2})
    assert resp.status_code == 200

    data = resp.json()
    assert len(data) == 1
    assert data[0]["topic_id"] == 2


def test_get_question_by_id_success(client, db_session: Session):
    q_id = seed_question(db_session)

    resp = client.get(f"/api/questions/{q_id}")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == q_id
    assert "question" in data
    assert "difficulty" in data
    assert "topic_id" in data


def test_get_question_by_id_not_found(client):
    resp = client.get("/api/questions/123456789")
    assert resp.status_code == 404