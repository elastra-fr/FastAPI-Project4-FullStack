from .database import engine
from fastapi import FastAPI, Request, status
from .routers import auth, todos, admin, users
from .models import Base
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse





app = FastAPI()

# Add the CORS middleware
origins = [

    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

#Create the database tables
Base.metadata.create_all(bind=engine)



# Add the static files
app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)  

@app.get("/healthy")
def health_check():
    return {"message": "Healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

