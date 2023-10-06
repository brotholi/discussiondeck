from sqlalchemy.sql import text
from flask import session
from db import db

def create_tag(tag, discussion_id):
    sql = "INSERT INTO tags (discussion_id, tag, created) VALUES (:discussion_id, :tag, NOW()) RETURNING id"
    db.session.execute(text(sql), {"discussion_id":discussion_id, "tag":tag})
    db.session.commit()
    return True

def get_tags():
    sql = "SELECT DISCTINCT tag FROM tags"
    result = db.session.execute(text(sql))
    tags = result.fetchall()
    return tags


def get_discussion_tags(discussion_id):
    sql = "SELECT DISTINCT tag FROM tags WHERE discussion_id=:discussion_id"
    result = db.session.execute(text(sql), {"discussion_id":discussion_id})
    discussion_tags = result.fetchall()
    return discussion_tags
