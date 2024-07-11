import sqlite3
import flask

import models

DATABASE_PATH = 'inventory.db'

app = flask.Flask(__name__)


def get_db():
    db = getattr(flask.g, '_database', None)
    if db is None:
        db = flask.g._database = sqlite3.connect(DATABASE_PATH)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()


@app.route('/egghead')
def root():
    get_db().cursor().execute('CREATE TABLE inventory(db_id, mfg_part_number, description)').close()
    return 'root page'

@app.route('/create/')
def create():
    db_id = flask.request.args.get('db_id')
    mfg_part_number = flask.request.args.get('mfg_part_number')
    description = flask.request.args.get('description')
    sql = f"INSERT INTO inventory VALUES ('{db_id}', '{mfg_part_number}', '{description}')"
    print(sql)
    db = get_db()
    db.cursor().execute(sql)
    db.commit()
    return 'create success!'


@app.route('/search')
def search():
    return 'search page'


@app.route('/view/<db_id>')
def view(db_id=None):
    res = get_db().cursor().execute(f"SELECT * FROM inventory WHERE db_id='{db_id}'")
    db_item = res.fetchone()
    print(db_item)
    item = models.Item(*db_item)
    return flask.render_template('view.html', item=item)
