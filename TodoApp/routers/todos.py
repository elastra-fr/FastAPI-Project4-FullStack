from .auth import get_current_user
from ..database import SessionLocal
from fastapi import APIRouter, Depends, Path, Request
from fastapi.exceptions import HTTPException
from ..models import Todo
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

# Create the templates object

templates = Jinja2Templates(directory="TodoApp/templates")

# Create the router
router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)


# Get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define the dependencies
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# Create the request model


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=75)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete: bool

def redirect_to_login():
    response=RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response


###Pages###

@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):


    try:
        user=await get_current_user(request.cookies.get("access_token"))
        print(user)
        if user is None:
            return redirect_to_login()
        
        todos=db.query(Todo).filter(Todo.owner_id==user.get("id")).all()
        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})
     
    except Exception as e:
        print("Error: ", e)
        return redirect_to_login()
    
    
@router.get("/add-todo-page")
async def render_add_todo_page(request: Request):
   try:
        user=await get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_to_login()
        return templates.TemplateResponse("add-todo.html", {"request": request, "user": user}) 
    
   except Exception as e:
        print("Error: ", e)
        return redirect_to_login()
    
@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user=await get_current_user(request.cookies.get("access_token"))
        if user is None:
            return redirect_to_login()
        todo=db.query(Todo).filter(Todo.id==todo_id).filter(Todo.owner_id==user.get("id")).first()
        return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})

    
    except Exception as e:
        print("Error: ", e)
        return redirect_to_login()



###Endpoints###

# Read all todo items
@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):

    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    return db.query(Todo).filter(Todo.owner_id == user.get("id")).all()


# Read a single todo item by id - With status code and Path parameter validation
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(
        Todo.owner_id == user.get("id")).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo item not found")


# Create a new todo item

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency,  db: db_dependency, todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    todo_model = Todo(
        **todo_request.model_dump(),
        owner_id=user.get("id")
    )
    db.add(todo_model)
    db.commit()


# Update a todo item by id - With status code and Path parameter validation

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, todo_request: TodoRequest, db: db_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(
        Todo.owner_id == user.get("id")).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo item not found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


# Delete a todo item by id - With status code and Path parameter validation

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(
        Todo.owner_id == user.get("id")).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo item not found")

    db.query(Todo).filter(Todo.id == todo_id).filter(
        Todo.owner_id == user.get("id")).delete()
    db.commit()
