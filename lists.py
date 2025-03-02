import db

def get_users_lists(user_id, page, page_size):
    sql = """SELECT lists.id, lists.title
             FROM lists
             WHERE user_id = ?
             ORDER BY id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    lists = db.query(sql, [user_id, limit, offset])
    return lists

def create_new_list(new_list_name, user_id):
    db.execute("""
               INSERT INTO lists
               (title, user_id)
               VALUES (?,?)
               """,[new_list_name, user_id])

def get_list(list_id):
    list = db.query("""
                    SELECT user_id, title
                    FROM lists
                    WHERE lists.id = ?
                    """, [list_id])
    return list if list else None

def get_items(list_id):
    return db.query("""
                    SELECT id, content, user_id
                    FROM items
                    WHERE list_id = ?
                    """, [list_id])

def get_item(item_id):
    return db.query("""
                    SELECT user_id
                    FROM items
                    WHERE id = ?
                    """,[ item_id])

def add_item_to_list(new_item_name, user_id, list_id):
    db.execute("""
               INSERT INTO items
               (content, user_id, list_id)
               VALUES (?,?,?)
               """, [new_item_name, user_id, list_id])
    return None

def remove_item(item_id):
    db.execute("DELETE FROM items WHERE id = ?", [item_id])

def remove_list(list_id):
    db.execute("DELETE FROM items WHERE list_id = ?", [list_id])
    db.execute("DELETE FROM lists WHERE id = ?", [list_id])

def search_list_count(user_id, search_word):
    return db.query("""
                    SELECT id
                    FROM lists
                    WHERE user_id = ?
                    AND title LIKE ?
                    """, [user_id,"%" + search_word + "%"])

def search_lists(user_id, search_word, page_size, page):
    limit = page_size
    offset = page_size * (page - 1)
    return db.query("""
                    SELECT id, title
                    FROM lists
                    WHERE user_id = ?
                    AND title LIKE ?
                    LIMIT ?
                    OFFSET ?
                    """, [user_id,"%" + search_word + "%", limit, offset])

def search_item_count(user_id, search_word):
    return db.query("""
                    SELECT DISTINCT i.id
                    FROM items as i, lists as li
                    WHERE i.content LIKE ?
                    AND i.user_id = ?
                    AND i.list_id = li.id
                    """, ["%" + search_word + "%", user_id])

def search_items(user_id, search_word, page_size, page):
    print("searchword:", search_word)
    limit = page_size
    offset = page_size * (page - 1)
    return db.query("""
                    SELECT DISTINCT
                    i.id AS item_id,
                    li.id AS list_id,
                    li.title
                    FROM
                    items AS i,
                    lists AS li
                    WHERE
                    i.content LIKE ?
                    AND i.user_id = ?
                    AND i.list_id = li.id
                    LIMIT ?
                    OFFSET ?
                    """, ["%" + search_word + "%", user_id, limit, offset])

def list_count(user_id):
    return db.query("""
                    SELECT COUNT(*)
                    FROM lists
                    WHERE user_id = ?
                    """, [user_id])