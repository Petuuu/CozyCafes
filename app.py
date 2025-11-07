from flask import Flask, request, session, render_template, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    r = db.query("SELECT id, comment FROM Reviews")
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

    query = "SELECT password_hash FROM users WHERE username = ?"
    password_hash = db.query(query, [uname])[0][0]

    if check_password_hash(password_hash, passwrd):
        session["username"] = uname
        return redirect("/")
    else:
        return render_template("login.html", error=True)


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    if request.method == "GET":
        return render_template("review.html")

    comment = request.form["comment"]
    db.execute("INSERT INTO Reviews (comment) VALUES (?)", [comment])
    return redirect("/")


@app.route("/edit_item/<int:id>", methods=["GET", "POST"])
def edit_item(id):
    if request.method == "GET":
        r = db.query("SELECT id, comment FROM Reviews WHERE id = ?", [id])
        return render_template("edit.html", review=r[0])

    edit = request.form["comment"]
    db.execute("UPDATE Reviews SET comment = ? where id = ?", [edit, id])
    return redirect("/")


@app.route("/delete_item/<int:review_id>")
def delete_item(review_id):
    db.execute("DELETE FROM Reviews WHERE id = ?", [review_id])
    return redirect("/")
