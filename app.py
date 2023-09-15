from flask import Flask, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2:///brotholi"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html", message="Discussion deck -keskustelualustalla voit luoda uusia keskustelujaketjuja.")

@app.route("/loginpage", methods=["POST"])
def loginpage():
    result = db.session.execute(text("SELECT content FROM messages"))
    messages = result.fetchall()
    return render_template("loginpage.html", username=request.form["username"],
                            messages=messages) 