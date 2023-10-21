import random
from flask import session
from sqlalchemy.sql import text
from db import db

def get_all_ads():
    sql = """SELECT id, advertiser, content, status, level, created, moderator_id
             FROM ads ORDER BY CREATED DESC"""
    result = db.session.execute(text(sql))
    ads = result.fetchall()
    return ads

def get_active_ads():
    sql = """SELECT id, advertiser, content, status, level, created, moderator_id
             FROM ads WHERE status=1 ORDER BY LEVEL"""
    result = db.session.execute(text(sql))
    ads = result.fetchall()
    return ads

def get_active_ad_by_level(level):
    sql = """SELECT id, advertiser, content, status, level, created, moderator_id
             FROM ads WHERE status=1 AND level=:level"""
    result = db.session.execute(text(sql), {"level":level})
    active_ad = result.fetchone()
    return active_ad

def show_ad():
    choices = [3] * 15 + [2] * 35 + [1] * 50
    shown = random.choice(choices)
    sql= """SELECT id, advertiser, content, status, level, created, moderator_id
            FROM ads WHERE status=1 AND level=:shown_level"""
    result = db.session.execute(text(sql), {"shown_level":shown})
    displayed_ad = result.fetchone()
    if not displayed_ad:
        return []
    return displayed_ad

def create_ad(arvertiser, content, level):
    moderator_id = session["user_id"]
    sql = """INSERT INTO ads (advertiser, content, status, level, created, moderator_id)
            VALUES (:arvertiser, :content, 0, :level, NOW(), :moderator_id)"""
    db.session.execute(text(sql), {"arvertiser":arvertiser, "content":content,
                                   "level":level, "moderator_id":moderator_id})
    db.session.commit()
    return True

def activate_ad(level, ad_id):
    deactivated_ad = get_active_ad_by_level(level)
    if deactivated_ad:
        if not deactivate_ad(deactivated_ad[0]):
            return False
    sql = "UPDATE ads SET status=1 WHERE id=:ad_id"
    db.session.execute(text(sql), {"ad_id":ad_id})
    db.session.commit()
    return True

def get_ad_information(ad_id):
    sql = """SELECT id, advertiser, content, status, level, created, moderator_id
             FROM ads WHERE id=:ad_id"""
    result = db.session.execute(text(sql), {"ad_id":ad_id})
    ad_information = result.fetchone()
    return ad_information

def deactivate_ad(ad_id):
    try:
        sql = "UPDATE ads SET status=0 WHERE id=:ad_id"
        db.session.execute(text(sql), {"ad_id":ad_id})
        db.session.commit()
        return True
    except:
        return False
    