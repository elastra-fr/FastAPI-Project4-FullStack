from .database import engine
from fastapi import FastAPI, Request
from .routers import auth, todos, admin, users
from .models import Base
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles





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

# Add the templates
templates = Jinja2Templates(directory="TodoApp/templates")

# Add the static files
app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")

@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/healthy")
def health_check():
    return {"message": "Healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

