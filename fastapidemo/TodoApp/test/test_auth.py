from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user
from jose import jwt
from datetime import timedelta
from fastapi import HTTPException
import pytest


app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, "test1234", db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user("nonexistent", "test1234", db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, "wrong_password", db)
    assert wrong_password_user is False


def test_create_access_token(test_user):
    username = 'testuser'
    user_id = 1
    role_user = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, expires_delta, role_user)

    decoded_token = jwt.decode(token, SECRET_KEY, 
                                algorithms=[ALGORITHM], 
                                options={"verify_signature": False})
    decoded_token_sub = decoded_token.get("sub")
    decoded_token_user_id = decoded_token.get("id")
    decoded_token_role = decoded_token.get("role")
    assert decoded_token_sub == username
    assert decoded_token_user_id == user_id
    assert decoded_token_role == role_user


@pytest.mark.asyncio
async def test_get_current_user_valid_token(test_user):
    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token)
    assert user == {'username': 'testuser', 'id': 1, 'user_role': 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload(test_user):
    encode = {'role': 'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as e:
        await get_current_user(token)
    assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert e.value.detail == "Could not validate credentials"


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(test_user):
    token = "invalid_token"

    with pytest.raises(HTTPException) as e:
        await get_current_user(token)
    assert e.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert e.value.detail == "Could not validate credentials"