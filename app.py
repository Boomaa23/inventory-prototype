import dotenv
import flask

import common
import models
from api_routes import api_blueprint
from root_routes import root_blueprint


dotenv.load_dotenv()
app = flask.Flask(__name__)

with app.app_context():
    _table_keys = ", ".join([f"'{k}'" for k in models.BLANK_ITEM.to_dict().keys()])
    common.get_db().cursor().execute(f'CREATE TABLE IF NOT EXISTS inventory({_table_keys})').close()

app.register_blueprint(api_blueprint)
app.register_blueprint(root_blueprint)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(flask.g, '_database', None)
    if db is not None:
        db.close()
