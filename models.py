from flask_sqlalchemy import SQLAlchemy

from app import app

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)


class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           nullable=False)
    product = db.relationship('Product',
                              backref=db.backref('discounts', lazy=False))

    # I understand that name, description and price are optional and will
    # default to self.product.(name,description,price) respectively
    product_name = db.Column(db.String(128), nullable=True)
    product_description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)

    discount = db.Column(db.Float, nullable=False)
    shipping_discount = db.Column(db.Float, nullable=False)
