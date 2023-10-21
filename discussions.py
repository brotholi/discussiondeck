from sqlalchemy.sql import text
from db import db
import users

def get_discussions():
    sql= """SELECT d.id, d.user_id, u.username, d.topic, d.created, d.likes
            FROM discussions d, users u WHERE d.visible=1 AND d.user_id = u.id 
            ORDER BY d.created DESC"""
    result = db.session.execute(text(sql))
    discussions = result.fetchall()
    return discussions

def create_discussion(topic, content):
    if not users.check_if_user_logged_in():
        return_values = [False]
        return return_values
    user_id = users.get_user_id()
    sql = """INSERT INTO discussions (user_id, topic, created, likes, content, visible)
             VALUES (:user_id, :topic, NOW(), 0, :content, 1) RETURNING id"""
    db.session.execute(text(sql), {"topic":topic, "user_id":user_id, "content":content})
    db.session.commit()
    sql = "SELECT LASTVAL()"
    result = db.session.execute(text(sql))
    discussion_id = result.fetchone()[0]
    return_values = [True, discussion_id]
    return return_values

def get_one_discussion(discussion_id):
    sql = """SELECT id, user_id, topic, created, likes, content
             FROM discussions WHERE id=:discussion_id AND visible=1"""
    result = db.session.execute(text(sql), {"discussion_id":discussion_id})
    discussion = result.fetchone()
    return discussion

def find_discussions_by_keyword(query):
    sql = """SELECT d.id, d.user_id, topic, d.created, d.likes FROM discussions d, tags t
             WHERE d.id = t.discussion_id AND d.visible=1
             AND (d.topic LIKE :keyword OR d.content LIKE :keyword OR t.tag LIKE :keyword)
             GROUP BY d.id ORDER BY d.created DESC"""
    result = db.session.execute(text(sql), {"keyword":"%"+query+"%"})
    discussions = result.fetchall()
    return discussions

def remove_discussion(discussion_id):
    sql = "UPDATE discussions SET visible=0 WHERE id=:discussion_id"
    db.session.execute(text(sql), {"discussion_id":discussion_id})
    db.session.commit()

def find_newest_discussion():
    sql = """SELECT id, user_id, topic, created, likes, content FROM discussions
             WHERE visible=1 ORDER BY created DESC LIMIT 1"""
    result = db.session.execute(text(sql))
    discussion = result.fetchone()
    return discussion
