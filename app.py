import math, time, markupsafe
from flask import Flask
from flask import abort, flash
from flask import redirect, render_template, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
import config, lists, userlogic, secrets

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/main")
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    login_check = userlogic.check_user(username, password)

    if not login_check:
        flash("VIRHE: väärä salasana tai tunnus")
        return redirect("/")
    else:
        session["username"] = username
        session["user_id"] = login_check
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/main")
        

@app.route("/logout")
def logout():
    require_login()
    del session["username"]
    del session["user_id"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html", filled={})

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return render_template("register.html", filled={"username": username})
    if password1 == "" or username == "":
        flash("VIRHE: käyttäjätunnus tai salasana ei voi olla tyhjä")
        return render_template("register.html", filled={})

    new_user = userlogic.create_new_user(username, password1)

    if new_user:
        flash("Tunnus luotu!")
        return redirect("/")
    else:
        flash("VIRHE: tunnus on jo varattu")
        return render_template("register.html", filled={"username": username})

@app.route("/main")
@app.route("/main/<int:page>")
def main(page=1):
    require_login()

    page_size = 10
    list_count = lists.list_count(session["user_id"])[0][0]
    page_count = math.ceil(list_count / page_size)

    if page < 1:
        return redirect("/main/1")
    if page > page_count and page_count > 0:
        return redirect("/main/" + str(page_count))

    users_lists = lists.get_users_lists(session["user_id"], page, page_size)

    return render_template("main.html",
                           list_count=list_count,
                           page=page,
                           page_count=page_count,
                           users_lists=users_lists,
                           page_size=page_size)

@app.route("/newlist", methods=["GET","POST"])
def newlist():
    require_login()
    if request.method == "GET":
        classes = lists.get_classes()
        return render_template("newlist.html", classes=classes)
    if request.method == "POST":
        check_csrf()
        class_assignation = request.form["class"]
        new_list_name = request.form["listname"]
        if not new_list_name or len(new_list_name) > 100:
            abort(403)
        lists.create_new_list(new_list_name, session["user_id"], class_assignation)
        return redirect("/main")

@app.route("/list/<int:list_id>", methods=["GET", "POST"])
def handle_lists(list_id):
    require_login()
    # check if access is authorized:
    list = lists.get_list(list_id)
    user_permission = lists.check_user_permission(list_id, session["user_id"])
    if not list:
        abort(404)
    if list[0]["user_id"] != session["user_id"] and len(user_permission) == 0:
        abort(403)

    if request.method == "GET":
        items = lists.get_items(list_id)
        comments = lists.get_comments(list_id)
        permissions = lists.get_permissions(list_id)
        return render_template("list.html",
                               list_owner=list[0]["list_owner"],
                               owner_id=list[0]["user_id"],
                               permissions=permissions,
                               user_permission=user_permission,
                               comments=comments,
                               items=items,
                               list_id=list_id,
                               list_name=list[0]["title"])

    if request.method == "POST":
        check_csrf()
        if list[0]["user_id"] != session["user_id"]:
            if user_permission[0]["sharetype"] != "2":
                abort(403)
        new_item_name = request.form["new_item_name"]
        if len(new_item_name) > 50:
            new_item_name = new_item_name[0:49]
        if new_item_name == "":
            return redirect("/list/"+str(list_id))    
        lists.add_item_to_list(new_item_name, session["user_id"], list_id)
        return redirect("/list/"+str(list_id))

@app.route("/remove_item/<int:item_id>", methods=["POST"])
def remove_item(item_id):
    require_login()
    check_csrf()
    referer_list_id = request.form["list_id"]
    # check if removing is authorized:
    item = lists.get_item(item_id)
    list_id = item[0]["list_id"]
    list_owner_id = lists.get_list(list_id)[0]["user_id"]
    user_permission = lists.check_user_permission(list_id, session["user_id"])
    if item[0]["user_id"] != session["user_id"]:
        if list_owner_id != session["user_id"]:
            if len(user_permission) == 0:
                abort(403)
            if user_permission[0]["sharetype"] != "2":
                abort(403)

    lists.remove_item(item_id)
    return redirect("/list/"+str(referer_list_id))

@app.route("/remove_list/<int:list_id>", methods=["GET", "POST"])
def remove_list(list_id):
    require_login()
    # check if removing is authorized:
    list = lists.get_list(list_id)
    if list[0]["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove.html", list_id=list_id)
    if request.method == "POST":
        check_csrf()
        if "continue" in request.form:
            lists.remove_list(list_id)
        return redirect("/main")

@app.route("/listsearch", methods=["GET"])
@app.route("/listsearch/<int:page>")
def search_lists(page=1):
    require_login()

    search_word = request.args.get("search_word")

    page_size = 10
    users_list = lists.list_count(session["user_id"], search_word) if search_word else []
    list_count = len(users_list)
    list_page_count = math.ceil(list_count / page_size)
    print("list_count: ", list_count)
    print("list_page_count: ", list_page_count)

    if page < 1:
        page = 1
    if page > list_page_count:
        page = list_page_count

    list_search = lists.get_users_lists(session["user_id"], page, page_size, search_word) if search_word else []

    return render_template("listsearch.html",
                           search_word=search_word,
                           list_search=list_search,
                           page=page,
                           list_page_count=list_page_count
                           )

@app.route("/itemsearch", methods=["GET"])
@app.route("/itemsearch/<int:page>")
def search_items(page=1):
    require_login()

    search_word = request.args.get("search_word")
    #get_item_count = lists.search_item_count(session["user_id"],
    #                                search_word) if search_word else []

    get_item_count = lists.search_items(session["user_id"], search_word) if search_word else []

    page_size = 10
    item_count = len(get_item_count)
    item_page_count = math.ceil(item_count / page_size)

    if page < 1:
        page = 1
    if page > item_page_count:
        page = item_page_count

    item_search = lists.search_items(session["user_id"],
                                     search_word,
                                     page_size,
                                     page
                                     ) if search_word else []

    return render_template("itemsearch.html",
                           search_word=search_word,
                           item_search=item_search,
                           page=page,
                           item_page_count=item_page_count
                           )

@app.route("/newcomment/<int:list_id>", methods=["POST"])
def newcomment(list_id):
    require_login()
    check_csrf()
    user_permission = lists.check_user_permission(list_id, session["user_id"])
    list = lists.get_list(list_id)
    if list[0]["user_id"] != session["user_id"]:
        if len(user_permission) == 0:
            abort(403)
        if user_permission[0]["sharetype"] != "2":
            abort(403)
    content = request.form["content"]
    if len(content) > 200:
        content = content[0:199]
    if content == "":
        return redirect("/list/" + str(list_id))    
    lists.new_comment(session["user_id"], content, list_id)
    return redirect("/list/" + str(list_id))

@app.route("/grantpermission/<int:list_id>", methods=["POST"])
def grantpermission(list_id):
    require_login()
    check_csrf()
    list = lists.get_list(list_id)
    if list[0]["user_id"] != session["user_id"]:
        abort(403)

    owner_id = request.form["owner_id"]
    recipient_id = lists.get_user_by_name(request.form["permitted_user"])
    if len(recipient_id) == 0:
        flash("Annettua käyttäjää ei löydy")
        return redirect("/list/" + str(list_id))
    recipient_id = recipient_id[0][0]
    permissions = lists.get_permissions(list_id)
    for i in permissions:
        if i["approved_user_id"] == recipient_id:
            flash("Et voi myöntää oikeuksia käyttäjälle, jolle niitä on jo myönnetty")
            return redirect("/list/" + str(list_id))
    list = lists.get_list(list_id)
    if list[0]["user_id"]  == recipient_id:
        flash("Et voi myöntää itsellesi käyttöoikeuksia")
        return redirect("/list/" + str(list_id))
    permission_type = request.form["permission_type"]

    lists.add_permission(
        list_id,
        owner_id,
        recipient_id,
        permission_type
    )
    return redirect("/list/" + str(list_id))

@app.route("/removepermission/<int:list_id>", methods=["POST"])
def remove_permission(list_id):
    require_login()
    check_csrf()
    list = lists.get_list(list_id)
    if list[0]["user_id"] != session["user_id"]:
        abort(403)

    permitted_user_id = request.form["permitted_user_id"]
    lists.remove_permission(list_id, permitted_user_id, session["user_id"])
    flash("Käyttöoikeus poistettu")
    return redirect("/list/" + str(list_id))