import sqlite3
import flask
import uuid
import json

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


@app.route('/init')
def init():
    get_db().cursor().execute('CREATE TABLE inventory(db_id, mfg_part_number, quantity, description, reserved)').close()
    return 'init page'

@app.route('/reserve')
def reserve():
    db_id = flask.request.args.get('db_id')
    name = flask.request.args.get('name')
    quantity = int(flask.request.args.get('quantity'))

    db = get_db()
    res = db.cursor().execute(f"SELECT reserved FROM inventory WHERE db_id='{db_id}'")
    db_item = res.fetchone()
    reserved = eval(db_item[0])
    if name in reserved:
        reserved[name] += quantity
    else:
        reserved[name] = quantity
    print(reserved)
    db.cursor().execute(f"UPDATE inventory SET reserved='{json.dumps(reserved)}' WHERE db_id='{db_id}'")
    db.commit()

    return 'reserve page'


@app.route('/create')
def create():
    item = models.Item(
        db_id=uuid.uuid4().hex[:16],
        mfg_part_number=flask.request.args.get('mfg_part_number'),
        quantity=flask.request.args.get('quantity'),
        description=flask.request.args.get('description'),
        reserved={}
    )
    print(item)
    db = get_db()
    db.cursor().execute(f"INSERT INTO inventory VALUES ({item.to_insert_str()})")
    db.commit()
    return f'create success! db_id={item.db_id}'


@app.route('/search')
def search():
    return 'search page'


@app.route('/view/<db_id>')
def view_single(db_id=None):
    res = get_db().cursor().execute(f"SELECT * FROM inventory WHERE db_id='{db_id}'")
    db_item = res.fetchone()
    item = models.Item(*db_item)
    return flask.render_template('view_single.html', item=item, view_url=flask.request.base_url)

@app.route('/view/reserved')
def view_reserved():
    res = get_db().cursor().execute("SELECT * FROM inventory WHERE reserved!='{}'")
    db_items = res.fetchall()
    items = [models.Item(*db_item) for db_item in db_items]
    return flask.render_template('view_multiple.html', items=items)

@app.route('/view/all')
def view_all():
    res = get_db().cursor().execute("SELECT * FROM inventory")
    db_items = res.fetchall()
    items = [models.Item(*db_item) for db_item in db_items]
    return flask.render_template('view_multiple.html', items=items)
