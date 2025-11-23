from flask import (
    Flask,
    request,
    session,
    render_template,
    redirect,
    abort,
    flash,
    make_response,
)
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex
from datetime import datetime
import sqlite3
import config
import db
import queries

app = Flask(__name__)
app.secret_key = config.secret_key


def check_exists(r):
    if not r:
        abort(404)


def check_allowed(r):
    if not session or r[0]["user"] != session["id"]:
        abort(403)


def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)


@app.route("/")
def index():
    r = queries.search_reviews()
    return render_template("index.html", reviews=r)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")

    uname = request.form["uname"]
    passwrd1 = request.form["passwrd1"]
    passwrd2 = request.form["passwrd2"]

    if passwrd1 != passwrd2:
        return render_template(
            "create.html", error="ERROR: passwords don't match", uname=uname
        )
    passwrd_hash = generate_password_hash(passwrd1)

    try:
        db.execute(
            "INSERT INTO Users (username, password_hash) VALUES (?, ?)",
            [uname, passwrd_hash],
        )
    except sqlite3.IntegrityError:
        return render_template("create.html", error="ERROR: username already exists")

    flash("Account successfully created")
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    uname = request.form["uname"]
    passwrd = request.form["passwrd"]

    try:
        query = db.query(
            "SELECT id, password_hash FROM users WHERE username = ?", [uname]
        )
        password_hash = query[0][1]

        if check_password_hash(password_hash, passwrd):
            session["uname"] = uname
            session["id"] = query[0][0]
            session["csrf_token"] = token_hex(16)
            return redirect("/")
        else:
            raise

    except:
        return render_template("login.html", error=True)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    if request.method == "GET":
        return render_template("review.html")

    check_csrf()
    cafe = request.form["cafe"]
    rating = request.form["rating"]
    text = request.form["text"]

    db.execute(
        """
        INSERT INTO
        Reviews (cafe, user, rating, review_text, date_created)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            cafe,
            session["id"],
            rating,
            text,
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        ],
    )
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")

    query = request.form["query"]
    r = search(query)
    return render_template("search.html", searched=True, reviews=r, query=query)


@app.route("/add_image", methods=["POST"])
def image():
    f = request.files["image"]
    if not f.filename.endswith(".jpg"):
        return profile(session["id"], error="ERROR: incorrect file type")

    image = f.read()
    if len(image) > 100 * 1024:
        return profile(session["id"], error="ERROR: image too large")

    db.execute("UPDATE Users SET pfp = ? WHERE id = ?", [image, session["id"]])
    return profile(session["id"])


@app.route("/image/<int:user>")
def show_image(user):
    r = db.query("SELECT pfp FROM Users WHERE id = ?", [user])
    if not r or r[0]["pfp"] is None:
        abort(404)

    response = make_response(r[0]["pfp"])
    response.headers.set("Content-Type", "image/jpeg")
    return response


@app.route("/profile/<int:user>")
def profile(user, error=None):
    u = queries.fetch_user(user)
    check_exists(u)
    r = queries.search_user_reviews(user)
    return render_template("profile.html", u=u[0], reviews=r, c=len(r), error=error)


@app.route("/edit_item/<int:id>", methods=["GET", "POST"])
def edit_item(id):
    if request.method == "GET":
        r = queries.fetch_review(id)
        check_exists(r)
        check_allowed(r)
        return render_template("edit.html", r=r[0])

    cafe = request.form["cafe"]
    rating = request.form["rating"]
    text = request.form["text"]

    db.execute(
        """
        UPDATE Reviews
        SET cafe = ?, rating = ?, review_text = ?, date_edited = ?
        WHERE id = ?
        """,
        [cafe, rating, text, datetime.now().strftime("%d-%m-%Y %H:%M:%S"), id],
    )
    return redirect("/")


@app.route("/delete_item/<int:review_id>", methods=["POST"])
def delete_item(review_id):
    db.execute("DELETE FROM Reviews WHERE id = ?", [review_id])
    return redirect("/")
