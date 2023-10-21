from sqlalchemy.sql import text
from db import db
import discussions
import users

def get_discussion_deck(discussion_id):
    discussion_info = discussions.get_one_discussion(discussion_id)
    username = users.find_username(discussion_info[1])
    discussion_deck = [discussion_info, username]
    return discussion_deck

def get_comments(discussion_id):
    sql = """SELECT c.id, c.user_id, u.username, c.discussion_id, c.comment, c.created, c.likes
             FROM comments c JOIN users u ON c.user_id = u.id 
             WHERE c.discussion_id=:discussion_id ORDER BY created DESC"""
    result = db.session.execute(text(sql), {"discussion_id":discussion_id})
    comments = result.fetchall()
    return comments

def like(user_id, discussion_id):
    if users.find_user_likes(user_id, discussion_id) == 0:
        sql = "UPDATE discussions SET likes = likes + 1 WHERE id=:discussion_id"
        db.session.execute(text(sql), {"discussion_id":discussion_id})
        sql = "INSERT INTO likes (user_id, discussion_id) VALUES (:user_id, :discussion_id)"
        db.session.execute(text(sql), {"user_id":user_id, "discussion_id":discussion_id})
        db.session.commit()
        return True
    return False

def comment(discussion_id, content):
    if not users.check_if_user_logged_in():
        return False
    user_id = users.get_user_id()
    sql = """INSERT INTO comments (user_id, discussion_id, comment, created, likes)
             VALUES (:user_id, :discussion_id, :comment, NOW(), 0) RETURNING ID"""
    db.session.execute(text(sql), {"user_id":user_id,
                                   "discussion_id":discussion_id, "comment":content})
    db.session.commit()
    return True
