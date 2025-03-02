import db

def get_users_lists(user_id, page, page_size):
    sql = """SELECT lists.* 
             FROM lists
             INNER JOIN users_lists
             ON lists.id = users_lists.list_id
             WHERE user_id = ?
             ORDER BY users_lists.id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    lists = db.query(sql, [user_id, limit, offset])
    return lists

def create_new_list(new_list_name,user_id):
    db.execute("INSERT INTO lists (title) VALUES (?)", [new_list_name])
    db.execute("INSERT INTO users_lists (list_id, user_id) VALUES (?,?)", [db.last_insert_id(),user_id])

def get_list(list_id):
    list = db.query("""SELECT lists.*,users_lists.user_id
             FROM lists,users_lists
             WHERE lists.id = ? AND users_lists.list_id = lists.id
            """, [list_id])
    return list if list else None

def get_items(list_id):
    return db.query("""SELECT items.id, items.content, users_lists.user_id AS user_id
                    FROM list_items, items, users_lists
                    WHERE items.id = list_items.item_id
                    AND users_lists.list_id = list_items.list_id
                    AND list_items.list_id = ?
                    """, [list_id])

def get_item(item_id):
    return db.query("""SELECT list_items.*, users_lists.*
                    FROM list_items, users_lists
                    WHERE list_items.item_id = ?
                    AND list_items.list_id = users_lists.list_id
                    """,[ item_id])

def add_item_to_list(new_item, list_id, user_id):
    db.execute("INSERT INTO items (content) VALUES (?)", [new_item])
    db.execute("""INSERT INTO list_items
               (item_id,list_id)
               VALUES (?,?)
               """, [db.last_insert_id(),list_id])
    return None

def remove_item(item_id):
    db.execute("DELETE FROM list_items WHERE item_id = ?", [item_id])

def remove_list(list_id):
    db.execute("DELETE FROM users_lists WHERE list_id = ?", [list_id])

def search_lists(user_id,search_word):
    return db.query("""SELECT users_lists.list_id AS id, lists.title
             FROM users_lists
             INNER JOIN lists
             ON users_lists.list_id = lists.id
             WHERE users_lists.user_id = ?
             AND lists.title LIKE ?
            """, [user_id,"%" + search_word + "%"])
    
def search_items(user_id,search_word):
    return db.query("""SELECT DISTINCT i.id AS item_id, li.list_id as list_id, l.title
                    FROM items as i, list_items as li, users_lists as u, lists AS l
                    WHERE i.content LIKE ?
                    AND u.user_id = ?
                    AND u.list_id = li.list_id
                    AND li.item_id = i.id
                    AND l.id = li.list_id
                    """, ["%" + search_word + "%", user_id])

def list_count(user_id):
    return db.query("""SELECT COUNT(*)
                    FROM users_lists
                    WHERE user_id = ?
                    """, [user_id])