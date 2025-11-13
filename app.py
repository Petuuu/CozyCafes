from flask import Flask, request, session, render_template, redirect, abort
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    r = db.query(
        """
        SELECT R.id, U.username, R.cafe, R.rating, R.review_text
        FROM Reviews R
        JOIN Users U ON U.id = R.user
        """
    )
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
            "INSERT INTO Reviews (cafe, user, rating, review_text) VALUES (?, ?, ?, ?)",
            [cafe, session["id"], rating, text],
        )
        return redirect("/")

    r = db.query("SELECT id, review_text FROM Reviews")
    return render_template("index.html", reviews=r, error=True)


@app.route("/edit_item/<int:id>", methods=["GET", "POST"])
def edit_item(id):
    r = db.query("SELECT id, review_text FROM Reviews WHERE id = ?", [id])
    if not r:
        abort(404)
    if not session or r[0][0] != session["id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", review=r[0])

    edit = request.form["text"]
    db.execute("UPDATE Reviews SET review_text = ? where id = ?", [edit, id])
    return redirect("/")


@app.route("/delete_item/<int:review_id>")
def delete_item(review_id):
    db.execute("DELETE FROM Reviews WHERE id = ?", [review_id])
    return redirect("/")
