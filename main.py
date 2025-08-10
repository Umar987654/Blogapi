from fastapi import FastAPI, BackgroundTasks
from routers import users, posts
from routers import upload
from routers import external
from database import create_db_and_tables

app = FastAPI()

def send_email_notification(email: str, message: str):
    print(f"Sending email to {email}: {message}")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/register")
def register_user(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_notification, email, "Thanks for registering!")
    return {"msg": "User registered"}

@app.get("/")
def read_root():
    return {"message": "API is working"}

   

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(upload.router)
app.include_router(external.router)

