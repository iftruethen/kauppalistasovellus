import db
from werkzeug.security import generate_password_hash, check_password_hash

def check_user(username, password):
    sql = "SELECT id, password_hash FROM users WHERE name = ?"
    user_details = db.query(sql,[username])

    if not user_details:
        return None
    
    if check_password_hash(user_details[0]["password_hash"], password):
        return user_details[0]["id"]
    

def create_new_user(username, password):
    sql = "INSERT INTO users (name, password_hash) VALUES (?,?)"
    db.execute(sql, [username, generate_password_hash(password)])