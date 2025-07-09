from db_connection import user_db, notes_db
import random

from faker import Faker
faker = Faker('en_IN')

# ================== user_db ===================


user=user_db()
for i in range(10):
    user.create(faker.name())


print(user.create("Gautam","g@gmail.com"))


single=user.find_one(password="12345")
all_user=user.find_all(password="12345")
print("Single user in db= ",single)


print("Total number of user in db= ",len(all_user))
print("Total user in db= ",all_user)


# ================== notes_db ===================

notes=notes_db()
user= user_db()
user_list = user.find_all()

for i in range(10):
    notes.create(title=faker.sentence(), content=faker.text(), user_id= random.choice(user_list)["_id"])
    
notes_list = notes.find_all()
print("Total number of notes in db= ", len(notes_list))
print("Total notes in db= ", notes_list)