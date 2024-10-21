from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status as statut
from ..models import Users

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == statut.HTTP_200_OK
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@test.com"
    assert response.json()["role"] == "admin"

def test_change_password_success(test_user):
    request_data = {
        "password": "password",
        "new_password": "newpassword"
    }
    response = client.put("/user/password", json=request_data)
    assert response.status_code == statut.HTTP_204_NO_CONTENT   

def test_change_password_fail(test_user):
    request_data = {
        "password": "wrongpassword",
        "new_password": "newpassword"
    }   

    response = client.put("/user/password", json=request_data)
    assert response.status_code == statut.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error: Incorrect password"}  


