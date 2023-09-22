from db import db
import users
from sqlalchemy.sql import text

def get_discussions():
    sql = "SELECT topic, created, likes FROM discussions ORDER BY created DESC"
    result = db.session.execute(text(sql))
    discussions = result.fetchall()
    return discussions

def create_discussion(topic):
    user_id = users.user_id()
    sql = "INSERT INTO discussions (user_id, topic, created, likes) VALUES (:user_id, :topic, NOW(), 0) RETURNING id"
    result = db.session.execute(text(sql), {"topic":topic, "user_id":user_id})
    discussion_id = result.fetchone()[0]
    db.session.commit()
    return discussion_id