import enum
import typing

import flask

import common


class Scope(enum.Enum):
    ITEM_GET = 0b1 << 0
    ITEM_CREATE = 0b1 << 1
    ITEM_UPDATE = 0b1 << 2
    ITEM_REMOVE = 0b1 << 3
    RESERVATION_GET = 0b1 << 4
    RESERVATION_CREATE = 0b1 << 5
    RESERVATION_UPDATE = 0b1 << 6
    RESERVATION_REMOVE = 0b1 << 7
    ITEMS_LIST = 0b1 << 8
    ITEMS_BULKADD = 0b1 << 9
    USER_GET = 0b1 << 10
    USER_CREATE = 0b1 << 11
    USER_UPDATE = 0b1 << 12
    USER_REMOVE = 0b1 << 13

    def __or__(self, other):
        return (self.value | other.value) if isinstance(other, Scope) else (self or other)

    def __and__(self, other):
        return (self.value & other.value) if isinstance(other, Scope) else (self or other)


def require_auth(req_authmask: typing.Union[Scope, int], user_db_id: str) -> None:
    if isinstance(req_authmask, Scope):
        req_authmask = req_authmask.value

    if common.is_dirty(user_db_id):
        flask.abort(400)

    res = common.get_db().cursor().execute(f"SELECT authmask FROM users WHERE db_id='{user_db_id}'")
    db_authmask = res.fetchone()

    if db_authmask is None or len(db_authmask) != 1:
        flask.abort(401)
    try:
        authmask = int(db_authmask[0])
        if (req_authmask & authmask) != req_authmask:
            flask.abort(403)
    except ValueError:
        flask.abort(500)
