from dotenv import load_dotenv
import os
import random
from datetime import datetime

# database connections
from pymongo import MongoClient
load_dotenv()

uri = str(os.getenv("DB_URI"))

class user_db:
    def __init__(self):
        self.client = MongoClient(uri)
        self.mydb= self.client["fastAPI_DB"]
        # table_name = "user_table"
       
  
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

   

class notes_db:
    def __init__(self):
        self.client = MongoClient(uri)
        self.mydb= self.client["fastAPI_DB"]
        self.table_name = "notes_table"
        # return self.mydb

    def create(self, title: str, content: str, user_id: str):
        note_data = {
            "title": title,
            "content": content,
            "user_id": user_id,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
        if self.find_one(title=note_data["title"]):
            return ValueError(f"Note with title '{note_data['title']}' already exists in database.")

        return self.mydb[self.table_name].insert_one(note_data)

    def find_one(self, **kwargs):
        note = self.mydb[self.table_name].find_one(kwargs)
        if note is None:
            return None
        return note
    
    def find_all(self, **kwargs):
        pointer = self.mydb[self.table_name].find(kwargs)
        if pointer is None:
            return []
        else:
            data = [i for i in pointer]
            return data

user = user_db()

user.create(name="Gautam", email="g@gmail.com")
u1=user.login(email="g@gmail.com",password="12345")
print(u1["_id"] if u1 else "User not found")
# print(u1["_id"])  # Assuming u1 is a dictionary with an "_id" key
notes = notes_db()

data={
    "title": "My First Note",
    "content": "This is the content of my first note.",
    "user_id": u1["_id"] if u1 else None  # Assuming u1 is a dictionary with an "_id" key
}
n1=notes.create(**data)

print("Note created with ID:", n1)


