from app import app
import decks
import users
from flask import redirect, render_template, request, session

@app.route("/")
def index():
    discussions = decks.get_discussions()
    all_users = users.get_all_users()
    return render_template("index.html", discussions=discussions, all_users=all_users)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("new.html")

    if request.method == "POST":
        topic = request.form["topic"]
        decks.create_discussion(topic)
        return redirect("/")

@app.route("/loginpage", methods=["GET", "POST"])
def loginpage():
    if request.method == "GET":
        return render_template("loginpage.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("error.html", message="Väärä käyttäjätunnus tai salasana")
        else:
            session["username"] = username
            return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.register(username, password):
            return render_template("error.html", message="Käyttäjätunnus on jo olemassa")
        else:
            return redirect("/loginpage")
    
    