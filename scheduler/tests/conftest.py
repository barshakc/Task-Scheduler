import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from scheduler.db.database import Base, get_db
from api.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
