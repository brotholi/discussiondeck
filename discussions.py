from sqlalchemy.sql import text
from db import db
import users

def get_discussions():
    sql= "SELECT d.id, d.user_id, u.username, d.topic, d.created, d.likes FROM discussions d JOIN users u ON d.user_id = u.id ORDER BY d.created DESC"
    result = db.session.execute(text(sql))
    discussions = result.fetchall()
    return discussions

def create_discussion(topic, content):
    #TODO tee tarkistus, että käyttäjä on kirjautunut paremmaksi
    user_id = users.get_user_id()
    number_of_users = users.find_user_id(user_id)
    if number_of_users == 0:
        return False
    sql = "INSERT INTO discussions (user_id, topic, created, likes, content) VALUES (:user_id, :topic, NOW(), 0, :content) RETURNING id"
    db.session.execute(text(sql), {"topic":topic, "user_id":user_id, "content":content})
    db.session.commit()
    return True

def get_one_discussion(discussion_id):
    sql = "SELECT id, user_id, topic, created, likes, content FROM discussions WHERE id=:discussion_id"
    result = db.session.execute(text(sql), {"discussion_id":discussion_id})
    discussion = result.fetchone()
    return discussion
    