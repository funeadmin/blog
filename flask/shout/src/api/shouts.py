from flask import Blueprint, jsonify, abort, request
from ..models import Shout, User, db

bp = Blueprint('shouts',__name__, url_prefix='/shouts')


@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    shouts = Shout.query.all() # ORM performs SELECT query
    result = []
    for s in shouts:
        result.append(s.serialize()) # build list of shouts as dictionaries
    return jsonify(result) # return JSON response

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    s = Shout.query.get_or_404(id, "Shout not found")
    return jsonify(s.serialize())

@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id and content
    if 'user_id' not in request.json or 'content' not in request.json:
        return abort(400)
    # user with id of user_id must exist
    User.query.get_or_404(request.json['user_id'], "User not found")
    # construct Shout
    s = Shout(
        user_id=request.json['user_id'],
        content=request.json['content']
    )
    db.session.add(s) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(s.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    s = Shout.query.get_or_404(id, "Shout not found")
    try:
        db.session.delete(s) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)

@bp.route('/<int:id>/liking_users', methods=['GET'])
def liking_users(id: int):
    s = Shout.query.get_or_404(id)
    result = []
    for u in s.liking_users:
        result.append(u.serialize())
    return jsonify(result)