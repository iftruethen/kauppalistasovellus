import db

def get_user_id(user):
    return db.query("SELECT id FROM users WHERE name = ?",[user])[0][0]

def get_users_lists(user):
    print(user)
    lists = db.query("SELECT * FROM lists WHERE user_id = ?",[get_user_id(user)])
    return lists

def create_new_list(new_list_name, user):
    db.execute("INSERT INTO lists (title, user_id) VALUES (?,?)",[new_list_name,get_user_id(user)])

def get_list(list_id):
    db.query("SELECT * FROM lists WHERE id = ?",[list_id])
    return None

def get_items(list_id):
    return db.query("SELECT * FROM list_items WHERE list_id = ?",[list_id])

def add_item_to_list(new_item, list_id, user):
    user_id = get_user_id(user)
    print("In logic module")
    print("new_item:", new_item)
    print("list_id: ", list_id)
    print("user_id: ", user_id)
    db.execute("INSERT INTO list_items (content,user_id,list_id) VALUES (?,?,?)",[new_item,user_id,list_id])
    return None