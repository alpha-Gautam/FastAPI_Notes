from pydantic import BaseModel
from uuid import UUID, uuid4

from dotenv import load_dotenv
import os
import random
from datetime import datetime

# database connections
from pymongo import MongoClient
load_dotenv()


uri = str(os.getenv("DB_URI"))


class user_schema(BaseModel):
    id: UUID | None = None
    name: str
    mobile: str | None = None
    email: str | None = None
    password: str | None = None



class User:
    def __init__(self):
        self.client = MongoClient(uri)
        self.mydb= self.client["fastAPI_DB"]
        # table_name = "user_table"
       
  
    def create_user(self,data: user_schema):
        email_prefix=data.name.split(" ")[0].strip().lower()
        if data.id is None:
            data.id = uuid4()
        user_data = {
            "name": data.name,
            "mobile": data.mobile or str(random.randint(1000000000, 9999999999)),
            "email": data.email or email_prefix+"@gmail.com",
            "password": data.password
        }
        
        if self.find_one(email=user_data["email"]):
            raise ValueError(f"User with this email'{user_data['email']}' already exists.")


        return self.mydb.user_table.insert_one(user_data)
    
    
    def create(self,name: str,mobile: str|None=None, email: str|None=None,password: str="12345"):
        email_prefix=name.split(" ")[0].strip().lower()
        
        user_data = {
            "name": name,
            "mobile": mobile or str(random.randint(1000000000, 9999999999)),
            "email": email or email_prefix+"@gmail.com",
            "password": password
        }
        
        if self.find_one(email=user_data["email"]):
            return ValueError(f"User with this email'{user_data['email']}' already exists.")
        
        
        return self.mydb.user_table.insert_one(user_data)
    
    def find_one(self, **kwargs):
        
        user = self.mydb.user_table.find_one(kwargs)
        if user is None:
            return None
        return user
    def find_all(self, **kwargs):

        pointer=self.mydb.user_table.find(kwargs)
        if pointer is None:
            return []
        else:
            data=[i for i in pointer]
            return data
    def login(self, email: str, password: str):
        user = self.find_one(email=email)
        if user and user.get("password") == password:
            return user
        elif user is None:
            return None

   

user1 = User()


data={
    "id": uuid4(),
    "name": "First Name",
    "mobile": "1234567890",
    "email":  None  # Assuming u1 is a dictionary with an "_id" key
    
}


asd=user1.create_user(user_schema(**data))

print(asd)


