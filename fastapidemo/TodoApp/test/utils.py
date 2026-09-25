from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todos, Users
from ..routers.auth import bcrypt_context

load_dotenv()

TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')

engine = create_engine(TEST_DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_create_user():
    return {"username": "codingwithroby", "email": "codingwithroby@email.com", "password": "test1234", "user_role": "admin", "id": 1}


client = TestClient(app)

@pytest.fixture()
def test_todo():
    todo = Todos(
        title="Learn to code",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos"))
        conn.commit()


def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"title": "Learn to code", 
                                "description": "Need to learn everyday!", 
                                "priority": 5, 
                                "complete": False, 
                                "owner_id": 1, "id": 1}]


@pytest.fixture()
def test_user():
    user = Users(
        username="codingwithroby",
        email="codingwithroby@email.com",
        first_name="Coding",
        last_name="Robby",
        hashed_password=bcrypt_context.hash("test1234"),
        role="admin",
        phone_number="(111)-111-1111",
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users"))
        conn.commit()


