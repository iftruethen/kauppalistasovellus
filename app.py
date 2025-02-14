import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db, lists

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT password_hash FROM users WHERE name = ?"
    password_element = db.query(sql, [username])
    
    if len(password_element) == 0:
        return render_template("message.html", message = "VIRHE: virheellinen tunnus")
    elif check_password_hash(password_element[0][0], password):
        session["username"] = username
        return redirect("/")
    else:
        return render_template("message.html", message="VIRHE: väärä salasana")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template("message.html", message="VIRHE: salasanat eivät ole samat")
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (name, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return render_template("message.html", message="Tunnus luotu")

@app.route("/main")
def main():
    users_lists = lists.get_users_lists(session["username"])
    print("from app.py", users_lists)
    return render_template("main.html", users_lists=users_lists)

@app.route("/newlist")
def newlist():
    return render_template("newlist.html")

@app.route("/createlist", methods=["POST"])
def createlist():
    new_list_name = request.form["listname"]
    lists.create_new_list(new_list_name,session["username"])
    #print("News list's name: ", new_list_name)
    return redirect("/main")

@app.route("/list/<int:list_id>", methods=["GET"])
def show_list(list_id):
    list = lists.get_list(list_id)
    items = lists.get_items(list_id)
    return render_template("list.html", list=list, items=items, list_id=list_id)

@app.route("/list/<int:list_id>", methods=["POST"])
def add_item_to_list(list_id):
    new_item = request.form["new_item"]
    lists.add_item_to_list(new_item, list_id, session["username"])
    return redirect("/list/"+str(list_id))