from sqlalchemy.orm import Session

from database import Topic


def test_root_endpoint(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json() == {"Hello": "World"}

# Would possibly remove this when I remove health endpoint
def test_healthz_endpoint(client):
    resp = client.get("/api/healthz")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_list_topics_empty(client):
    resp = client.get("/api/topics")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_topics_with_data(client, db_session: Session):
    topic = Topic(name="Fluids", slug="fluids")
    db_session.add(topic)
    db_session.commit()

    resp = client.get("/api/topics")
    assert resp.status_code == 200
    data = resp.json()

    assert len(data) == 1
    assert data[0]["name"] == "Fluids"
    assert data[0]["slug"] == "fluids"
    assert "id" in data[0]
