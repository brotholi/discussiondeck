import os
from db import db
from flask import session, request, abort
import secrets
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def get_all_users():
    sql = "SELECT id, username FROM users"
    result = db.session.execute(text(sql))
    users = result.fetchall()
    return users

def login(username, password):
    sql = "SELECT id, password, role FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return_values = [False, "Väärä käyttäjätunnus"]
        return return_values

    if not check_password_hash(user[1], password):
        return_values = [False, "Väärä salasana"]
        return return_values
    session["user_id"] = user[0]
    session["username"] = username
    session["user_role"] = user[2]
    session["csrf_token"] = secrets.token_hex(16)
    session.permanent = True
    return_values = [True]
    return return_values

    
def register(username, password1, role):
    if check_if_user_exists(username):
        return False
    password_hash = generate_password(password1)
    sql = "INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"
    db.session.execute(text(sql), {"username":username, "password":password_hash, "role":role})
    db.session.commit()
    login(username, password1)
    return True

def logout():
    del session["username"]
    del session["user_id"] 
    del session["user_role"]
    del session["csrf_token"]
    session.permanent = False

def get_user_id():
    return session.get("user_id", 0)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

def generate_password(password):
    hash_value = generate_password_hash(password)
    return hash_value
    
def check_if_user_exists(username):
    sql = "SELECT COUNT(*) FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    count = result.fetchone()[0]
    if count == 0:
        return False
    return True

def find_username(user_id):
    sql = "SELECT username FROM users WHERE id=:user_id"
    result = db.session.execute(text(sql), {"user_id":user_id})
    username = result.fetchone()[0]
    return username

def find_user_id(user_id):
    sql = "SELECT COUNT(*) FROM users WHERE id=:user_id"
    result = db.session.execute(text(sql), {"user_id":user_id})
    user_id = result.fetchone()[0]
    return user_id

def check_role(role):
    if role > session.get("user_role", 0):
        abort(403)

def find_user_likes(user_id, discussion_id):
    sql = "SELECT COUNT(*) FROM likes WHERE user_id=:user_id AND discussion_id=:discussion_id"
    result = db.session.execute(text(sql), {"user_id":user_id, "discussion_id":discussion_id})
    likes = result.fetchone()[0]
    return likes