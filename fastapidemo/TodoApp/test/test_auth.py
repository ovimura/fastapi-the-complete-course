from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import timedelta


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
    decoded_token_user_id = decoded_token.get("user_id")
    decoded_token_role = decoded_token.get("role")
    assert decoded_token_sub == username
    assert decoded_token_user_id == user_id
    assert decoded_token_role == role_user
