from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
reviews = []


@app.route("/")
def index():
    return render_template("index.html", reviews=reviews)


@app.route("/review")
def review():
    return render_template("review.html")


@app.route("/result", methods=["POST"])
def result():
    reviews.append(request.form["comment"])
    return redirect(url_for("index"))
