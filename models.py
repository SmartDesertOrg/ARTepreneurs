from enum import unique
from flask_login import UserMixin
from sqlalchemy.orm import backref
from wtforms.validators import ValidationError
from config import db, app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), unique=True, nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), unique=True, nullable=False)
    address = db.Column(db.Text, unique=True)
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.Integer)
    def __repr__(self):
        return f"User '{self.user_id}','{self.fname}', '{self.email}'"


    def get_reset_token(self, expires_sec=300):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_id(self):
        return (self.user_id)
class Art(db.Model):
    item_id = db.Column(db.Integer,primary_key=True)
    artist_name = db.Column(db.String(50),nullable=False)
    title = db.Column(db.String(50),nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    images = db.Column(db.String(20), nullable=False, default='default.jpg')
    price = db.Column(db.Float, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    item_quantity = db.Column(db.Integer, nullable=False, default=1)
    counter = db.Column(db.Integer)
    cartitem = db.relationship('CartItem', backref='Product')
    def __repr__(self):
        return f"Art '{self.item_id}', '{self.artist_name}', '{self.title}','{self.description}','{self.category}','{self.images}','{self.price}','{self.item_quantity}'"


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer,db.ForeignKey('art.item_id'))
    title = db.Column(db.String(50),nullable=False)
    artist_name = db.Column(db.String(50),nullable=False)
    images = db.Column(db.String(20), nullable=False, default='default.jpg')
    price = db.Column(db.Float, nullable=False)
    item_quantity = db.Column(db.Integer, nullable=False, default=1)
    def __repr__(self):
        return f"Cart '{self.product_id}', '{self.artist_name}', '{self.title}','{self.images}','{self.price}','{self.item_quantity}'"
