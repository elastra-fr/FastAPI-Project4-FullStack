from .utils import *
from ..routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM, get_current_user  
from fastapi import status as statut
from ..models import Users
from jose import jwt
from datetime import datetime, timedelta
import pytest
from fastapi import HTTPException


app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
    db= TestingSessionLocal()

    authenticated_user= authenticate_user(db, test_user.username, "password")
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user= authenticate_user(db, "nonexistent", "password")
    assert non_existent_user is False

    wrong_password_user= authenticate_user(db, test_user.username, "wrongpassword")
    assert wrong_password_user is False


def test_create_access_token(test_user):
    token= create_access_token(test_user.username, test_user.id, test_user.role, timedelta(minutes=15))
    assert token is not None

    decoded= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
    assert decoded["sub"] == test_user.username
    assert decoded["id"] == test_user.id
    assert decoded["role"] == test_user.role
    assert datetime.fromtimestamp(decoded["exp"]) > datetime.now()

@pytest.mark.asyncio
async def test_get_current_user_valid_token(test_user):
    encode= {"sub": test_user.username, "id": test_user.id, "role": test_user.role}
    token= jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user= await get_current_user(token)  
    assert user== {"username": test_user.username, "id": test_user.id, "role": test_user.role}

@pytest.mark.asyncio
async def test_get_current_user_missing_payload(test_user):
    encode = {"role":"user"}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    with pytest.raises(HTTPException) as e:
        await get_current_user(token=token)
    assert e.value.status_code == statut.HTTP_401_UNAUTHORIZED
    assert e.value.detail == "Could not validate credentials"

    