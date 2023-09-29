from sqlalchemy.sql import text
from db import db
import discussions
import users

def get_discussion_deck(discussion_id):
    discussion_info = discussions.get_one_discussion(discussion_id)
    username = users.find_username(discussion_info[1])
    #TODO comments = get_comments(discussion_id)
    discussion_deck = [discussion_info, username]
    return discussion_deck

def get_comments(discussion_id):
    sql = "SELECT id, user_id, discussion_id, comment, created, likes FROM comments WHERE discussion_id=:discussion_id ORDER BY created DESC"
    result = db.session.execute(text(sql), {"discussion_id":discussion_id})
    comments = result.fetchall()
    return comments

def like(discussion_id):
    try:
        sql = "UPDATE discussions SET likes = likes + 1 WHERE id=:discussion_id"
        db.session.execute(text(sql), {"discussion_id":discussion_id})
        db.session.commit()
        return True
    except:
        return False