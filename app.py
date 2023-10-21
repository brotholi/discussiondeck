from flask import Flask
from datetime import timedelta
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.permanent_session_lifetime = timedelta(minutes=5)


import routes
