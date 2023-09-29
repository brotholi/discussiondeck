from app import app
from flask import redirect, render_template, request, url_for
import discussions
import users
import decks

@app.route("/")
def index():
    all_discussions = discussions.get_discussions()
    all_users = users.get_all_users()
    return render_template("index.html", discussions=all_discussions, all_users=all_users)

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
        content = request.form["content"]
        if len(topic) == 0:
            return render_template("error.html", 
                                   message="Keskusteluaihe ei voi olla tyhjä")
        if len(content) == 0:
            return render_template("error.html", 
                                   message="Viesti ei voi olla tyhjä")
        create_discussion= discussions.create_discussion(topic, content)
        if not create_discussion:
            return render_template("error.html", 
                                   message="Kirjaudu tai luo käyttäjä ennen viestin luomista")
        return redirect("/discussions")
    
@app.route("/discussions")
def show_discussions():
        all_discussions = discussions.get_discussions()
        return render_template("discussions.html", discussions=all_discussions)

@app.route("/discussions/<int:discussion_id>")
def show_discussion(discussion_id):
    discussion_information = decks.get_discussion_deck(discussion_id)
    return render_template("deck.html", discussion_information=discussion_information)

@app.route("/discussions/<int:discussion_id>/like", methods=["POST"])
def like(discussion_id):
    if not decks.like(discussion_id):
        return render_template("error.html", 
                               message="Tykkäys ei onnistunut")
    return redirect(url_for('show_discussion',discussion_id = discussion_id))