
from ..routers.todos import get_db, get_current_user
from fastapi import status as statut
from .utils import *





app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user




def test_read_all_authenticated(test_todo):
    response = client.get("/todos")
    assert response.status_code == statut.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "title": "Test Todo",
        "description": "Test Description",
        "priority": 1,
        "complete": False,
        "owner_id": 1
    }]

def test_read_one_authenticated(test_todo):
    response = client.get("/todos/todo/1")
    assert response.status_code == statut.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "title": "Test Todo",
        "description": "Test Description",
        "priority": 1,
        "complete": False,
        "owner_id": 1
    }

def test_read_one_authenticated_not_found():
    response = client.get("/todos/todo/999")
    assert response.status_code == statut.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo item not found"}


def test_create_todo(test_todo):
    request_data = {
        "title": "Test Todo 2",
        "description": "Test Description 2",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }
    response = client.post("/todos/todo", json=request_data)
    assert response.status_code == statut.HTTP_201_CREATED 

    db= TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id == 2).first()
    assert model.title == "Test Todo 2"  
    assert model.description == "Test Description 2"
    assert model.priority == 5
    assert model.complete == False

def test_update_todo(test_todo):
    request_data = {
        "title": "Change Todo 2",
        "description": "Change Description 2",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }
    response = client.put("/todos/todo/1", json=request_data)
    assert response.status_code == statut.HTTP_204_NO_CONTENT

    db= TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id == 1).first()
    assert model.title == "Change Todo 2"  
    assert model.description == "Change Description 2"
    assert model.priority == 5
    assert model.complete == False

def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "Change Todo 2",
        "description": "Change Description 2",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }
    response = client.put("/todos/todo/999", json=request_data)
    assert response.status_code == statut.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo item not found"} 

def test_delete_todo(test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == statut.HTTP_204_NO_CONTENT

    db= TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id == 1).first()
    assert model == None

def test_delete_todo_not_found(test_todo):
    response = client.delete("/todos/todo/999")
    assert response.status_code == statut.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo item not found"}

