from pydantic import BaseModel
from uuid import UUID, uuid4





class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None



class User:
    def __init__(self, name: str, email: str|None=None,password: str ="12345"):
        if not name or not email:
            raise ValueError("Name and email cannot be empty")
        self.name = name
        self.email = email or self.name+"@gmail.com"
        self.password = password
        
    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, password={self.password})"
    
    def create_user(self):
        return {
            # "id": str(uuid4()),
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

