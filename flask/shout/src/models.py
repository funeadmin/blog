import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
            # 'password': self.password  do not want this line because it will print actuall password to screen
        }


likes_table = db.Table(
    'likes',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'shout_id', db.Integer,
        db.ForeignKey('shouts.id'),
        primary_key=True
    ),
    db.Column(
        'created_at', db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
)


class Shout(db.Model):
    __tablename__ = 'shouts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(280), nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    liking_users = db.relationship(
        'User', secondary=likes_table,
        lazy='subquery',
        backref=db.backref('liked_shouts', lazy=True)
    )

    def __init__(self, content: str, user_id: int):
        self.content = content
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id
        }
