from datetime import datetime
from math import ceil
import sqlite3
from secrets import token_hex
from json import dumps, loads
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
import config
import db
import queries

app = Flask(__name__)
app.secret_key = config.SECRECT_KEY
page_size = 8


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
@app.route("/<int:page>")
def index(page=1):
    rows = queries.search_review_count()[0][0]
    page_count = ceil(rows / page_size) if rows else 1

    if page < 1:
        return redirect("/1")
    elif page > page_count:
        return redirect(f"/{page_count}")

    rows = queries.search_page_reviews(page, page_size)
    reviews = []

    for r in rows:
        review = {k: r[k] for k in r.keys()}
        review["categories"] = loads(r["categories"]) if r["categories"] else None
        reviews.append(review)

    return render_template(
        "index.html", page=page, page_count=page_count, reviews=reviews
    )


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
        return render_template("login.html", error=True)

    except IndexError:
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
    categories = dumps(request.form.getlist("categories"))

    db.execute(
        """
        INSERT INTO
        Reviews (cafe, user, rating, review_text, categories, date_created)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            cafe,
            session["id"],
            rating,
            text,
            categories,
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        ],
    )
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")

    query = request.form["query"]
    rows = queries.search(query)

    reviews = []
    for r in rows:
        review = {k: r[k] for k in r.keys()}
        review["categories"] = loads(r["categories"]) if r["categories"] else None
        reviews.append(review)

    return render_template("search.html", searched=True, reviews=reviews, query=query)


@app.route("/add_image", methods=["POST"])
def image():
    f = request.files["image"]
    if not f.filename.endswith(".jpg"):
        return profile(session["id"], error="ERROR: incorrect file type")

    img = f.read()
    if len(img) > 100 * 1024:
        return profile(session["id"], error="ERROR: image too large")

    db.execute("UPDATE Users SET pfp = ? WHERE id = ?", [img, session["id"]])
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
    rows = queries.search_user_reviews(user)

    reviews = []
    for r in rows:
        review = {k: r[k] for k in r.keys()}
        review["categories"] = loads(r["categories"]) if r["categories"] else None
        reviews.append(review)

    return render_template(
        "profile.html", u=u[0], reviews=reviews, c=len(rows), error=error
    )


@app.route("/edit_item/<int:review_id>", methods=["GET", "POST"])
def edit_item(review_id):
    if request.method == "GET":
        r = queries.fetch_review(review_id)
        check_exists(r)
        check_allowed(r)

        row = r[0]
        review = {k: row[k] for k in row.keys()}
        review["categories"] = loads(row["categories"]) if row["categories"] else None

        return render_template("edit.html", r=review)

    cafe = request.form["cafe"]
    rating = request.form["rating"]
    text = request.form["text"]
    categories = dumps(request.form.getlist("categories"))

    db.execute(
        """
        UPDATE Reviews
        SET cafe = ?, rating = ?, review_text = ?, categories = ?, date_edited = ?
        WHERE id = ?
        """,
        [
            cafe,
            rating,
            text,
            categories,
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            review_id,
        ],
    )
    return redirect("/")


@app.route("/delete_item/<int:review_id>", methods=["POST"])
def delete_item(review_id):
    r = queries.fetch_review(review_id)
    check_exists(r)
    check_allowed(r)

    db.execute("DELETE FROM Reviews WHERE id = ?", [review_id])

    return redirect("/")


@app.route("/comments/<int:comm_id>", methods=["GET", "POST"])
def comments(comm_id):
    r = queries.fetch_review(comm_id)
    check_exists(r)

    if request.method == "GET":
        c = queries.search_comments(comm_id)
        return render_template("comments.html", r=r[0], coms=c)

    check_csrf()
    db.execute(
        """
        INSERT INTO Comments (review, user, comment, date_created)
        VALUES (?, ?, ?, ?)
        """,
        [
            comm_id,
            session["id"],
            request.form["comment"],
            datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        ],
    )
    return redirect(f"/comments/{comm_id}")


@app.route("/delete_comment/<int:comm_id>", methods=["POST"])
def delete_comment(comm_id):
    r = queries.fetch_comment_section(comm_id)
    check_exists(r)
    check_allowed(r)

    r_id = r[0]["review"]
    db.execute("DELETE FROM Comments WHERE id = ?", [comm_id])

    return redirect(f"/comments/{r_id}")
