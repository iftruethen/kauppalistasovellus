import db

def get_users_lists(user_id, page=None, page_size=None, search_term=""):
    sql= """
        SELECT DISTINCT user_lists.*, COUNT(items.id) as item_count

        FROM
        (
        SELECT lists.id, lists.title, users.name AS list_owner, classes.class AS class_name
        FROM lists, users, classes
        WHERE user_id = ?
        AND users.id = lists.user_id
        AND lists.title LIKE ?
        AND classes.id = lists.class_id

        UNION ALL

        SELECT shares.list_id AS id, lists.title, users.name AS list_owner, classes.class AS class_name
        FROM shares, lists, users, classes
        WHERE approved_user_id = ?
        AND lists.id = shares.list_id
        AND users.id = shares.owner_user_id
        AND lists.title LIKE ?
        AND classes.id = lists.class_id
        ) AS user_lists
        
        LEFT JOIN items
        ON items.list_id = user_lists.id
        GROUP BY user_lists.id

        ORDER BY user_lists.id DESC
        """
    params = [user_id, "%" + search_term + "%", user_id, "%" + search_term + "%"]
    if page and page_size:
        sql = sql + "\nLIMIT ? OFFSET ?"
        limit = page_size
        offset = page_size * (page - 1)
        params.append(limit)
        params.append(offset)
    lists = db.query(sql, params)
    return lists

def create_new_list(new_list_name, user_id, class_assignation):
    db.execute("""
               INSERT INTO lists
               (title, user_id, class_id)
               VALUES (?,?,?)
               """,[new_list_name, user_id, class_assignation])

def get_list(list_id):
    list = db.query("""
                    SELECT
                    l.user_id AS user_id,
                    l.title AS title,
                    u.name AS list_owner
                    FROM lists AS l, users AS u
                    WHERE l.id = ?
                    AND u.id = l.user_id
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
                    SELECT user_id, list_id
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
    db.execute("DELETE FROM lists WHERE id = ?", [list_id])

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

def search_items(user_id, search_word, page_size=None, page=None):
    sql = """
        SELECT DISTINCT
        i.id AS item_id,
        l.id AS list_id,
        l.title AS list_name,
        c.class AS class_name,
        u.name AS list_owner,
        i.content AS item_name,
        (SELECT COUNT(id) AS item_count FROM items WHERE items.list_id=l.id) AS item_count
        FROM items AS i, lists AS l, classes AS c, users u
        LEFT JOIN shares AS s
        ON s.list_id = l.id
        WHERE i.content LIKE ?
        AND i.list_id = l.id
        AND c.id = l.class_id
        AND u.id = l.user_id
        AND (l.user_id = ? OR s.approved_user_id = ?)
        """
    params = ["%" + search_word + "%", user_id, user_id]
    if page and page_size:
        limit = page_size
        offset = page_size * (page - 1)
        params.append(limit)
        params.append(offset)
        sql = sql + "\nLIMIT ? OFFSET ?"
    oldsql = """
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
        """
    return db.query(sql, params)

def list_count(user_id, searchword=None):
    params = [user_id, user_id]
    if not searchword:
        sql = """
            SELECT COUNT(user_id)
            FROM 
            (
                SELECT user_id 
                FROM lists 
                WHERE user_id = ?

                UNION ALL 

                SELECT approved_user_id AS user_id 
                FROM shares 
                WHERE approved_user_id = ?
            )
            """
    else:
        params = [user_id, searchword, user_id, searchword]
        sql = """
            SELECT COUNT(user_id)
            FROM 
            (
                SELECT user_id 
                FROM lists 
                WHERE user_id = ?
                AND lists.title LIKE ?

                UNION ALL 

                SELECT approved_user_id AS user_id 
                FROM shares, lists
                WHERE approved_user_id = ?
                AND lists.id = shares.list_id
                AND lists.title LIKE ?
            )
            """
    return db.query(sql, params)

def new_comment(user_id, content, list_id):
    sql = """
            INSERT INTO comments (content, user_id, list_id)
            VALUES (?,?,?)
        """
    db.execute(sql, [content, user_id, list_id])

def get_comments(list_id):
    return db.query("""
                    SELECT c.content AS content, u.name AS user
                    FROM comments AS c, users AS u
                    WHERE c.list_id = ?
                    AND u.id = c.user_id
                    """, [list_id])

def add_permission(list_id, owner_id, recipient_id, permission_type):
    sql = """
            INSERT INTO shares
            (list_id, owner_user_id, approved_user_id, sharetype)
            VALUES (?,?,?,?)
        """
    db.execute(sql, [list_id, owner_id, recipient_id, permission_type])

def get_permissions(list_id):
    return db.query("""
                    SELECT s.approved_user_id,
                    s.sharetype,
                    u.name
                    FROM shares AS s, users AS u
                    WHERE s.list_id = ?
                    AND u.id = s.approved_user_id
                    """, [list_id])

def remove_permission(list_id, permitted_user_id, owner_id):
    db.execute("""
               DELETE FROM shares
               WHERE list_id = ?
               AND approved_user_id = ?
               AND owner_user_id = ?
               """, [list_id, permitted_user_id, owner_id])

def check_user_permission(list_id, user_id):
    sql = """
    SELECT approved_user_id, sharetype
    FROM shares
    WHERE list_id = ?
    AND approved_user_id = ?
    """
    return db.query(sql, [list_id, user_id])

def get_user_by_name(username):
    return db.query("SELECT id FROM users WHERE name = ?",
                    [username])

def get_classes():
    return db.query("SELECT id, class FROM classes")