import db

def get_users_lists(user, user_id):
    lists = db.query("SELECT lists.* FROM lists INNER JOIN users_lists ON lists.id = users_lists.list_id  WHERE user_id = ?",[user_id])
    return lists

def create_new_list(new_list_name,user_id):
    db.execute("INSERT INTO lists (title) VALUES (?)",[new_list_name])
    db.execute("INSERT INTO users_lists (list_id, user_id) VALUES (?,?)",[db.last_insert_id(),user_id])

def get_list(list_id):
    db.query("SELECT * FROM lists WHERE id = ?",[list_id])
    return None

def get_items(list_id):
    return db.query("""SELECT items.id,items.content FROM list_items 
                    LEFT JOIN items
                    ON items.id = list_items.item_id
                    WHERE list_id = ?""",[list_id])

def add_item_to_list(new_item, list_id, user_id):
    db.execute("INSERT INTO items (content) VALUES (?)",[new_item])
    db.execute("INSERT INTO list_items (item_id,list_id) VALUES (?,?)",[db.last_insert_id(),list_id])
    return None

def remove_item(item_id):
    db.execute("DELETE FROM list_items WHERE item_id = ?",[item_id])

def remove_list(list_id):
    db.execute("DELETE FROM users_lists WHERE list_id = ?",[list_id])

def search_lists(user_id,search_word):
    return db.query("""SELECT users_lists.*, lists.title
             FROM users_lists
             INNER JOIN lists
             ON users_lists.list_id = lists.id
             WHERE users_lists.user_id = ?
             AND lists.title LIKE ?""",[user_id,"%"+search_word+"%"])
    