import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from server import app

os.environ["TESTING"] = "1"  # prevent seed logic in server/database

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def clean_db():
    # Truncate all tables before each test for isolation
    session = TestingSessionLocal()
    try:
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
    finally:
        session.close()
    yield

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

class FakeUser:
    def __init__(self, id=1, username="testuser", email="test@example.com"):
        self.id = id
        self.username = username
        self.email = email

@pytest.fixture
def fake_user():
    return FakeUser()


# AI generated fixture to override require_user
@pytest.fixture(autouse=False)
def override_require_user(fake_user):
    # Only used in tests that need it
    from services.auth import require_user
    app.dependency_overrides[require_user] = lambda: fake_user
    yield fake_user
    app.dependency_overrides.pop(require_user, None)

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c