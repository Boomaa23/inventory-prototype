import flask
import sqlite3


DATABASE_PATH = 'inventory.db'


def get_db():
    db = getattr(flask.g, '_database', None)
    if db is None:
        db = flask.g._database = sqlite3.connect(DATABASE_PATH)
    return db
