from flask_sqlalchemy import SQLAlchemy

from .app import app
from .exceptions import NotFoundError

db = SQLAlchemy(app)

class Product(db.Model):
    """
    Skeleton Product model to be used in the Promotion relation
    """
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

    @classmethod
    def from_json(cls, promotion_json, create_products=False):
        product_ids = set(map(lambda prom: prom.get('product_id'),
                              promotion_json))
        products = {
            p.id: p
            for p in Product.query.filter(Product.id.in_(product_ids))
        }

        for promotion in promotion_json:
            product = products.get(promotion['product_id'])
            if not product:
                if not create_products:
                    raise NotFoundError('Product {} not found'.format(
                        promotion['product_id']))
