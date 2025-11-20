from flask import Flask, request, session, render_template, redirect, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3
import config
import db
import reviews

app = Flask(__name__)
app.secret_key = config.secret_key


def check_exists_and_allowed(r):
    if not r:
        abort(404)
    if session and r[0] == session["id"]:
        abort(403)


@app.route("/")
def index():
    r = reviews.search_reviews()
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
            return redirect("/")
        else:
            raise

    except:
        return render_template("login.html", error=True)


@app.route("/logout")
def logout():
    del session["uname"]
    del session["id"]
    return redirect("/")


@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    if request.method == "GET" and session:
        return render_template("review.html")

    if request.method == "POST":
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

    r = reviews.search_reviews()
    return render_template("index.html", reviews=r, error=True)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")

    query = request.form["query"]
    r = search(query)
    return render_template("search.html", searched=True, reviews=r[::-1], query=query)


@app.route("/edit_item/<int:id>", methods=["GET", "POST"])
def edit_item(id):
    if request.method == "GET":
        r = reviews.fetch_review(id)
        check_exists_and_allowed(r)
        return render_template("edit.html", review=r[0])

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
