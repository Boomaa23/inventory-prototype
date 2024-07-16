import flask

from api_routes import api_blueprint
from root_routes import root_blueprint


app = flask.Flask(__name__)
app.register_blueprint(api_blueprint)
app.register_blueprint(root_blueprint)


# @api_blueprint.route('/api/init')
# def init():
#     common.get_db().cursor().execute('CREATE TABLE inventory(db_id, mfg_part_number, quantity, description, reserved)').close()
#     return 'init page'


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()
