from .utils import *
from ..routers.users import get_current_user, get_db
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_create_user


def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == test_user.id
    assert response.json()['username'] == test_user.username
    assert response.json()['email'] == test_user.email
    assert response.json()['first_name'] == test_user.first_name
    assert response.json()['last_name'] == test_user.last_name
    assert response.json()['role'] == test_user.role
    assert response.json()['phone_number'] == test_user.phone_number



