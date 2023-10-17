from app import app
from flask import redirect, render_template, request, url_for, session
import discussions
import users
import decks
import extras

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
            
        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Tuntematon käyttäjärooli")    


        if not users.register(username, password1, role):
            return render_template("error.html", 
                                   message="Käyttäjätunnus on jo käytössä")
        return redirect("/")
    
@app.route("/result")
def result():
    query = request.args["query"]
    result = discussions.find_discussions_by_keyword(query)

    return render_template("result.html", discussions=result)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("new.html", tags=[])
    if request.method == "POST":
        users.check_csrf()
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
        return render_template("tags.html")
    
@app.route("/discussions")
def show_discussions():
        all_discussions = discussions.get_discussions()
        return render_template("discussions.html", discussions=all_discussions)

@app.route("/discussions/<int:discussion_id>", methods=["GET"])
def show_discussion(discussion_id):
    if request.method == "GET":
        discussion_information = decks.get_discussion_deck(discussion_id)
        discussion_comments = decks.get_comments(discussion_id)
        if len(discussion_comments) <= 5:
            deck_comments = discussion_comments
        else:
            deck_comments = discussion_comments[:5]
        return render_template("deck.html", discussion_information=discussion_information, comments=deck_comments)

@app.route("/discussions/<int:discussion_id>/like", methods=["POST"])
def like(discussion_id):
    if not decks.like(discussion_id):
        return render_template("error.html", 
                               message="Tykkäys ei onnistunut")
    return redirect(url_for('show_discussion',discussion_id = discussion_id))

@app.route("/discussions/<int:discussion_id>/all_comments", methods=["GET", "POST"])
def comment(discussion_id):
    if request.method == "GET":
        discussion_comments = decks.get_comments(discussion_id)
        deck_comments = discussion_comments
        return render_template("comment.html", comments=deck_comments, discussion_id=discussion_id)
    if request.method == "POST":
        users.check_csrf()
        comment_content = request.form["content"]
        if len(comment_content ) == 0:
            return render_template("error.html", 
                                message="Kommentti ei voi olla tyhjä")
        if not decks.comment(discussion_id, comment_content):
            return render_template("error.html", 
                                message="Kirjaudu tai luo käyttäjä ennen kommentin lisäämistä")
        return redirect(url_for('show_discussion', discussion_id = discussion_id))
    

@app.route("/tags", methods=["GET", "POST"])
def tags():
    if request.method == "GET":
        return render_template("tags.html", discussion_tags=[])
    if request.method == "POST":
        users.check_csrf()
        tag = request.form["tag"]
        if len(tag) == 0:
            return render_template("error.html", 
                                message="Tunniste ei voi olla tyhjä")
        all_discussions = discussions.get_discussions()
        newest_discussion = all_discussions[0]
        id = newest_discussion[0]
        if len(extras.get_discussion_tags(id)) == 5:
            return render_template("error.html", message="Tunnisteita ei voi olla yli viisi")
        else:
            extras.create_tag(tag, id)
            discussion_tags = extras.get_discussion_tags(id)
            return render_template("tags.html", tags = discussion_tags)
        
@app.route("/discussions/<int:discussion_id>/delete", methods=["POST", "GET"])
def delete(discussion_id):
    if request.method == "GET":
        return render_template("delete.html",discussion_id=discussion_id)
    
    if request.method == "POST":
        users.check_csrf()
        user_id = users.get_user_id()
        if not discussions.remove_discussion(discussion_id, user_id):
            return render_template("error.html", 
                                   message="Viestin poistaminen ei onnistunut")
        return redirect(url_for("show_discussions"))