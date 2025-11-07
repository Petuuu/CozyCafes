from flask import Flask, request, render_template, redirect
import db

app = Flask(__name__)


@app.route("/")
def index():
    r = db.query("SELECT comment FROM Reviews")
    return render_template("index.html", reviews=r)


@app.route("/review")
def review():
    return render_template("review.html")


@app.route("/send", methods=["POST"])
def result():
    comment = request.form["comment"]
    db.execute("INSERT INTO Reviews (comment) VALUES (?)", [comment])
    return redirect("/")
