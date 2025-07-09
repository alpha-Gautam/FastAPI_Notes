# from typing import Union

from fastapi import FastAPI
from db_connection import user_db, notes_db

app = FastAPI()


@app.get("/")
def read_root():
    
    return {"Hello": "World"}

@app.get("/api/login/")
def login(email: str | None = None, password: str | None = None):
    if email is None or password is None:
        return {"error": "Email and password are required"}
    user = user_db()
    user_data = user.login(email=email, password=password)
    if user_data is None:
        return {"error": "Invalid email or password"}
    return {**user_data}

@app.post("/api/create_user/")
def create_user(request):
    data= request.json()
    if not data.get("name") or not data.get("email") or not data.get("password"):
        return {"error": "Name, email, and password are required"}
    user = user_db()
    user_data = user.create(**data)
    if isinstance(user_data, ValueError):
        return {"error": str(user_data)}
    return {"message": "User created successfully", "user_id": str(user_data.inserted_id)}

@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: str | None = None, s: str | None = None):
    return {"item_id": item_id, "q": q, "s": s}