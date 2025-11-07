import sqlite3
from flask import g


def get_connection():
    db = sqlite3.connect("database.db")
    db.execute("PRAGMA foreign_keys = ON")
    db.row_factory = sqlite3.Row
    return db


def last_insert_id():
    return g.last_insert_id


def execute(query, params=[]):
    db = get_connection()
    r = db.execute(query, params)
    db.commit()
    g.last_insert_id = r.lastrowid
    db.close()


def query(query, params=[]):
    db = get_connection()
    r = db.execute(query, params).fetchall()
    db.close()
    return r
