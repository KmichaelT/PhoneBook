from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def get_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #contacts=db.relationship('Contacts',backref='author',lazy=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User|{self.username}>"

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Contacts(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30),  nullable=False)
    address=db.Column(db.String(30), nullable=False)
    phone=db.Column(db.Numeric(12,0), nullable=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    def __repr__(self):
        return f"Contacts('{self.name}','{self.phone}','{self.address}') "

    def add(self):
        db.session.add(self)
        db.session.commit()