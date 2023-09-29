from sqlalchemy.sql import text
from db import db
import users

def get_discussions():
    sql = "SELECT topic, created, likes FROM discussions ORDER BY created DESC"
    result = db.session.execute(text(sql))
    discussions = result.fetchall()
    return discussions

def create_discussion(topic):
    user_id = users.get_user_id()
    number_of_users = users.find_user_id(user_id)
    if number_of_users == 0:
        return False
    sql = "INSERT INTO discussions (user_id, topic, created, likes) VALUES (:user_id, :topic, NOW(), 0) RETURNING id"
    db.session.execute(text(sql), {"topic":topic, "user_id":user_id})
    db.session.commit()
    return True

def get_discussion_information(discussion_id):
    pass
