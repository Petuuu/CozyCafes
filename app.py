from flask import Flask, request, render_template, redirect
import db

app = Flask(__name__)


@app.route("/")
def index():
    r = db.query("SELECT id, comment FROM Reviews")
    return render_template("index.html", reviews=r)


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
