import flask
import uuid
import json

import models
import common


api_blueprint = flask.Blueprint('api', __name__)


@api_blueprint.route('/api/item/get/<db_id>', methods=['GET'])
def api_item_get(db_id):
    res = common.get_db().cursor().execute(f"SELECT * FROM inventory WHERE db_id='{db_id}'")
    db_item = res.fetchone()
    item = models.Item(*db_item)
    return item.to_dict()


@api_blueprint.route('/api/item/create', methods=['POST'])
def api_item_create():
    item = models.Item(
        db_id=uuid.uuid4().hex[:16],
        mfg_part_number=flask.request.form['mfg_part_number'],
        quantity=flask.request.form['quantity'],
        description=flask.request.form['description'],
        reserved={}
    )
    db = common.get_db()
    db.cursor().execute(f"INSERT INTO inventory VALUES ({item.to_insert_str()})")
    db.commit()
    return item.to_dict()


@api_blueprint.route('/api/item/update', methods=['POST'])
def api_item_update():
    pass


@api_blueprint.route('/api/item/remove', methods=['POST'])
def api_item_remove():
    pass


@api_blueprint.route('/api/reservation/get/<db_id>', methods=['GET'])
def api_reservation_get(db_id):
    pass


@api_blueprint.route('/api/reservation/create', methods=['POST'])
def api_reservation_create():
    db_id = flask.request.args.get('db_id')
    name = flask.request.args.get('name')
    quantity = int(flask.request.args.get('quantity'))

    db = common.get_db()
    res = db.cursor().execute(f"SELECT reserved FROM inventory WHERE db_id='{db_id}'")
    db_item = res.fetchone()

    reserved = eval(db_item[0])
    if name in reserved:
        reserved[name] += quantity
    else:
        reserved[name] = quantity

    db.cursor().execute(f"UPDATE inventory SET reserved='{json.dumps(reserved)}' WHERE db_id='{db_id}'")
    db.commit()

    return 'reserve page'


@api_blueprint.route('/api/reservation/update', methods=['POST'])
def api_reservation_update():
    pass


@api_blueprint.route('/api/reservation/remove', methods=['POST'])
def api_reservation_remove():
    pass


@api_blueprint.route('/api/items/list', methods=['GET'])
def api_items_list():
    res = common.get_db().cursor().execute("SELECT * FROM inventory")
    db_items = res.fetchall()
    items = [models.Item(*db_item) for db_item in db_items]
    return [item.to_dict() for item in items]


@api_blueprint.route('/api/items/bulkadd', methods=['POST'])
def api_items_bulkadd():
    pass