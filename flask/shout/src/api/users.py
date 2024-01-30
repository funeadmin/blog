# prior from flask import Blueprint
from flask import Blueprint, jsonify, abort, request
from ..models import User, db, Tweet, likes_table
import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    users = User.query.all() # ORM performs SELECT query
    result = []
    for u in users:
        result.append(u.serialize()) # build list of User as dictionaries
    return jsonify(result) # return JSON response
    
@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    u = User.query.get_or_404(id, "User not found")
    return jsonify(u.serialize())

@bp.route('', methods=['POST'])
def create():
    # req body must contain username and password
    if 'username' not in request.json and 'password' not in request.json:
        return abort(400)
    if len('username') <= 3 or len('password') <= 8 in request.json:
        return abort(400)
    
    # contstruct User 
    u = User(
        username=request.json['username'],
        password=scramble(request.json['password'])    # scramble password being passed
    )
    
    db.session.add(u) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(u.serialize())
    
@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    u = User.query.get_or_404(id, "User not found")
    try:
        db.session.delete(u) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)

@bp.route('/<int:id>', methods=['PATCH','PUT'])
def update(id: int):
    u = User.query.get_or_404(id)
        
    # req body must contain username and password
    if 'username' not in request.json and 'password' not in request.json:
        return abort(400)
    if len('username') >= 3 in request.json: 
        u.username=request.json['username']
        return u.username
    if len('password') >= 8 in request.json:
        u.password=scramble(request.json['password'])    
        return u.password 
    else: 
        abort(400)   
    
    try:
       db.session.add(u) # prepare CREATE statement
       db.session.commit() # execute CREATE statement
       return jsonify(u.serialize())  
    except: 
        # something went wrong :(
        return jsonify(False)
    
@bp.route('/<int:id>/liked_tweets', methods=['GET'])
def liked_tweets(id: int):
    u = User.query.get_or_404(id)
    result = []
    for t in u.liked_tweets:
        result.append(t.serialize())
    return jsonify(result)