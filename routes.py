from app import app
from flask import redirect, render_template, request, session
import decks
import users

@app.route("/")
def index():
    discussions = decks.get_discussions()
    all_users = users.get_all_users()
    return render_template("index.html", discussions=discussions, all_users=all_users)

@app.route("/loginpage", methods=["GET", "POST"])
def loginpage():
    if request.method == "GET":
        return render_template("loginpage.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        login = users.login(username, password)
        if not login[0]:
            return render_template("error.html", 
                                   message=login[1])
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html", 
                                   message="Käyttäjätunnus oltava 3-20 merkkiä pitkä")
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 == "":
            return render_template("error.html", 
                                   message="Salasana ei voi olla tyhjä")
        if password1 != password2:
            return render_template("error.html", 
                                   message="Salasanat eivät täsmää")

        if not users.register(username, password1):
            return render_template("error.html", 
                                   message="Käyttäjätunnus on jo käytössä")
        return redirect("/loginpage")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("new.html")
    if request.method == "POST":
        # users.check_csrf()

        topic = request.form["topic"]
        if len(topic) == 0:
            return render_template("error.html", 
                                   message="Keskusteluaihe ei voi olla tyhjä")
        create_discussion= decks.create_discussion(topic)
        if not create_discussion:
            return render_template("error.html", 
                                   message="Kirjaudu tai luo käyttäjä ennen viestin luomista")
        return redirect("/discussions")
    
@app.route("/discussions")
def discussions():
        discussions = decks.get_discussions()
        return render_template("discussions.html", discussions=discussions)

@app.route("/discussion/<int:discussion_id>")
def show_discussion(discussion_id):
    discussion_information = decks.get_discussion_information(discussion_id)
    return render_template("open.html", discussion_information=discussion_information)