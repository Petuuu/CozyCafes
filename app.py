from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    db = sqlite3.connect("database.db")
    reviews = db.execute("SELECT comment FROM Reviews").fetchall()
    db.close()
    return render_template("index.html", reviews=reviews)


@app.route("/review")
def review():
    return render_template("review.html")


@app.route("/send", methods=["POST"])
def result():
    comment = request.form["comment"]

    db = sqlite3.connect("database.db")
    db.execute("INSERT INTO Reviews (comment) VALUES (?)", [comment])
    db.commit()
    db.close()
    return redirect("/")
