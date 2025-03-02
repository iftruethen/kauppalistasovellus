import random
import sqlite3
import sys

db = sqlite3.connect("db.db")

user_count = 1000
list_count = 10**5
item_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (name, password_hash) VALUES (?,?)",
               ["user" + str(i),"foobar"])
    
db_user_ids = db.execute("""SELECT id FROM users""").fetchall()

for i in range(1, list_count + 1):
    db.execute("INSERT INTO lists (title, user_id) VALUES (?,?)",
               ["list" + str(i),
                db_user_ids[random.randint(0,len(db_user_ids)-1)][0]])

list_ids = db.execute("SELECT id FROM lists").fetchall()

for i in range(1, item_count + 1):
    random_list_id = list_ids[random.randint(0,len(list_ids)-1)][0]
    list_owner_user_id = db.execute("SELECT user_id FROM lists WHERE id = ?", [random_list_id]).fetchall()[0][0]
    db.execute("""INSERT INTO items (content, user_id, list_id) VALUES (?,?,?)""",
               ["item" + str(i),
                list_owner_user_id,
                random_list_id])

db.commit()
db.close