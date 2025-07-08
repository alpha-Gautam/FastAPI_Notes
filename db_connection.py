from dotenv import load_dotenv
import os
import random

# database connections
from pymongo import MongoClient
# myclient = MongoClient("mongodb+srv://gautammauryamail:R44GrJoMauAjN2yS@cluster0.hk9okct.mongodb.net/")
load_dotenv()

uri = str(os.getenv("DB_URI"))

class user_db:
    def __init__(self):
        self.client = MongoClient(uri)
        self.mydb= self.client["fastAPI_DB"]
       
    def db_table(self):
        return self.mydb.user_table
    
    def db_name(self):
        return self.mydb
    
    def userdb_name(self):
        return "fastAPI_DB"
    
    def create(self,name: str, email: str|None=None,password: str="12345"):
        email_prefix=name.split(" ")[0].strip().lower()
        user_data = {
            "name": name,
            "email": email or email_prefix+str(random.randint(100, 999))+"@gmail.com",
            "password": password
        }
        return self.mydb.user_table.insert_one(user_data)
    
    def find_user(self, **kwargs):
        return self.mydb.user_table.find(kwargs)

class notes_db:
    def __init__(self):
        self.client = MongoClient(uri)
        self.mydb= self.client["fastAPI_DB"]
        return self.mydb.notes_table
        # return self.mydb

    def db_name(self):
        return self.mydb
    
    def userdb_name(self):
        return "fastAPI_DB"




user = user_db()
print(user.create("Gautam","g@gmail.com"))


db=user.find_user(password="12345")
print(db)
users = []
for i in db:
    users.append(i)
    
    
print("Total user in db= ",len(users))
print(users)