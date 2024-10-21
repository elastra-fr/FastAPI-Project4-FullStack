from .utils import *
from ..routers.admin import get_db, get_current_user
from fastapi import status as statut
from ..models import Todo


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == statut.HTTP_200_OK
    assert response.json() == [{
        "id": 1,
        "title": "Test Todo",
        "description": "Test Description",
        "priority": 1,
        "complete": False,
        "owner_id": 1
    }]

def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == statut.HTTP_204_NO_CONTENT

    db= TestingSessionLocal()
    model = db.query(Todo).filter(Todo.id == 1).first()
    assert model == None

def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/999")
    assert response.status_code == statut.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo item not found"}