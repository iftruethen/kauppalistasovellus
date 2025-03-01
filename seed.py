import random
import sqlite3
import sys

db = sqlite3.connect("db.db")

user_count = 1000
list_count = 10**5
item_count = 10**6

# default password for dummy users is (without quotes): "abc"
default_password_hash = """scrypt:32768:8:1$RhBOzqjOYkLbYOUd$40ea92f847a0cf09953b0b3aba494d9b731aecc55720cd5f91f66652fc1a7ea34cc66e9a2ac56765e0a2b6508c041615c982b81147eeb5cb9075ab979549807"""

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (name, password_hash) VALUES (?, ?)",
               ["user" + str(i),default_password_hash])
    
user_ids = []
db_user_ids = db.execute("""SELECT id FROM users""").fetchall()
for i in db_user_ids:
    user_ids.append(i[0])


for i in range(1, list_count + 1):
    db.execute("INSERT INTO lists (title) VALUES (?)",
               ["list" + str(i)])
    last_list_id = db.execute("SELECT MAX(id) FROM lists").fetchall()[0][0]

    something = random.randint(0,len(user_ids)-1)
    random_user_id = user_ids[random.randint(0,len(user_ids)-1)]
    db.execute("""INSERT INTO users_lists (list_id, user_id) VALUES (?, ?)""", [last_list_id,random_user_id])


for i in range(1, item_count + 1):
    user_id = random.randint(1, user_count)
    list_id = random.randint(1, list_count)
    db.execute("""INSERT INTO items (content) VALUES (?)""",["item" + str(i)])
    last_item_id = db.execute("SELECT MAX(id) FROM items").fetchall()[0][0]
    random_list_id = db.execute("SELECT id FROM lists LIMIT 1 OFFSET ?", [list_id-1]).fetchall()[0][0]
    db.execute("""INSERT INTO list_items (item_id, list_id)
               VALUES (?,?)""", [last_item_id, random_list_id])

db.commit()
db.close