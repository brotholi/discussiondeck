from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def get_all_users():
    sql = "SELECT id, username FROM users"
    result = db.session.execute(text(sql))
    users = result.fetchall()
    return users

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()    
    if not user:
#incorrect username
        return False
    else:
        hash_value = user.password
    if check_password_hash(hash_value, password):
#correct password
        session["user_id"] = user[0]
        session["user_name"] = username
        return True
    else:
#incorrect password 
        return False
    
def register(username, password):
    if check_if_user_exists(username):
        return False

    password_hash = generate_password(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(text(sql), {"username":username, "password":password_hash})
    db.session.commit()
    return True

def user_id():
    return session.get("user_id", 0)

def generate_password(password):
    hash_value = generate_password_hash(password)
    return hash_value
    
def check_if_user_exists(username):
    sql = "SELECT COUNT(*) FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    count = result.fetchone()[0]
    if count == 0:
        return False
    else:
        return True

