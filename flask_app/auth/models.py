from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class User(database.Model, UserMixin ):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(100), unique=True, nullable=False)
    password_hash = database.Column(database.String(300), nullable=False)
    role = database.Column(database.String(10), default='user')

    def __init__(self, username, password_hash, role='user'):
        self.username = username
        self.password_hash = password_hash
        self.role=role

    def __repr__(self):
        return '<User %r>' % self.username

