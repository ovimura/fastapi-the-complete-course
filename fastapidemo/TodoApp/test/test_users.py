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



def test_change_password_success(test_user):
    response = client.put("/user/password", json={"password": "test1234", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_password(test_user):
    response = client.put("/user/password", json={"password": "invalid_password", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == "Incorrect password."

def test_change_phone_number_success(test_user):
    response = client.put("/user/phonenumber/2222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT