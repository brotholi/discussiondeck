from app import app
from flask import redirect, render_template, request, url_for, session
import discussions
import users
import decks
import tags
import ads

@app.route("/")
def index():
    newest_discussions = discussions.get_discussions()
    if len(newest_discussions) < 5:
        newest_discussions = newest_discussions
    else:
        newest_discussions = newest_discussions[:5]
    all_users = users.get_all_users()
    displayable_ad = ads.show_ad()
    return render_template("index.html", newest_discussions=newest_discussions,
                           all_users=all_users, displayable_ad=displayable_ad)

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
def query_result():
    query = request.args["query"]
    if len(query) < 3:
        return render_template("error.html",
                               message="Hakusanan oltava vähintään 3 merkkiä pitkä")
    result = discussions.find_discussions_by_keyword(query)
    return render_template("result.html", result=result)

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
        deck_tags = tags.get_discussion_tags(discussion_id)
        discussion_comments = decks.get_comments(discussion_id)
        if len(discussion_comments) <= 5:
            deck_comments = discussion_comments
        else:
            deck_comments = discussion_comments[:5]
        return render_template("deck.html", discussion_information=discussion_information,
                               deck_tags=deck_tags, comments=deck_comments)

@app.route("/discussions/<int:discussion_id>/like", methods=["POST"])
def like(discussion_id):
    users.check_csrf()
    user_id = users.get_user_id()
    if not decks.like(user_id, discussion_id):
        return render_template("error.html",
                               message="Olet jo tykännyt keskustelusta")
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
def create_discussion_tags():
    if request.method == "GET":
        return render_template("tags.html")
    if request.method == "POST":
        users.check_csrf()
        tag = request.form["tag"]
        if len(tag) == 0:
            return render_template("error.html",
                                message="Tunniste ei voi olla tyhjä")
        all_discussions = discussions.get_discussions()
        newest_discussion = all_discussions[0]
        discussion_id = newest_discussion[0]
        if len(tags.get_discussion_tags(discussion_id)) == 5:
            return render_template("error.html", message="Tunnisteita ei voi olla yli viisi")
        tags.create_tag(tag, discussion_id)
        deck_tags = tags.get_discussion_tags(discussion_id)
        return render_template("tags.html", deck_tags=deck_tags)

@app.route("/discussions/<int:discussion_id>/delete", methods=["POST", "GET"])
def delete(discussion_id):
    if request.method == "GET":
        return render_template("delete.html",discussion_id=discussion_id)

    if request.method == "POST":
        users.check_csrf()
        user_id = users.get_user_id()
        if discussions.get_one_discussion(discussion_id)[1] != user_id:
            users.check_role(2)
        discussions.remove_discussion(discussion_id)
        return redirect(url_for("show_discussions"))

@app.route("/ads")
def advertisments():
    all_ads = ads.get_all_ads()
    active_ads = ads.get_active_ads()
    return render_template("ads.html", all_ads=all_ads, active_ads=active_ads)

@app.route("/new_ad", methods=["GET", "POST"])
def new_advertisment():
    if request.method == "GET":
        return render_template("new_ad.html")
    if request.method == "POST":
        users.check_csrf()
        advertiser = request.form["advertiser"]
        content = request.form["content"]
        if len(advertiser) == 0:
            return render_template("error.html",
                                   message="Mainostajan nimi ei voi olla tyhjä")
        if len(content) == 0:
            return render_template("error.html",
                                   message="Mainoksen sisältö ei voi olla tyhjä")
        if "level" not in request.form:
            return render_template("error.html",
                                   message="Valitse mainoksen taso")
        level = request.form["level"]
        if not ads.create_ad(advertiser, content, level):
            return render_template("error.html",
                                   message="Mainoksen luominen ei onnistunut")
        return redirect(url_for("advertisments"))

@app.route("/ads/<int:ad_id>")
def advertisement_information(ad_id):
    ad_info = ads.get_ad_information(ad_id)
    return render_template("ad_info.html", ad_info=ad_info)

@app.route("/ads/<int:ad_id>/activate", methods=["GET","POST"])
def activate_ad(ad_id):
    if request.method == "GET":
        ad_information = ads.get_ad_information(ad_id)
        level = ad_information[4]
        now_active = ads.get_active_ad_by_level(level)
        return render_template("activate.html", ad_id=ad_id, ad_information=ad_information,
                               now_active=now_active)
    if request.method == "POST":
        users.check_csrf()
        level = ads.get_ad_information(ad_id)[4]
        if not ads.activate_ad(level, ad_id):
            return render_template("error.html",
                                message="Mainoksen aktivointi ei onnistunut")
        return redirect(url_for("advertisments"))

@app.route("/ads/<int:ad_id>/deactivate", methods=["POST"])
def deactivate_ad(ad_id):
    users.check_csrf()
    if not ads.deactivate_ad(ad_id):
        return render_template("error.html",
                                message="Mainoksen deaktivointi ei onnistunut")
    return redirect(url_for("advertisments"))
