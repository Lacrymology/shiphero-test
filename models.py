from flask_sqlalchemy import SQLAlchemy

from app import app
from exceptions import NotFoundError, ForbiddenError

db = SQLAlchemy(app)

class User(db.Model):
    """
    Skeleton User model
    """
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_dummy(cls):
        """
        Returns a Dummy User for use in tests
        """
        user = cls.query.get(0)
        if user is None:
            user = User(id=0)
            db.session.add(user)
            db.session.commit()
        return user


class Product(db.Model):
    """
    Skeleton Product model to be used in the Promotion relation
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('products', lazy=True))

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)


class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           nullable=False)
    product = db.relationship('Product',
                              backref=db.backref('discounts', lazy=True))

    # I understand that name, description and price are optional and will
    # default to self.product.(name,description,price) respectively
    product_name = db.Column(db.String(128), nullable=True)
    product_description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)

    discount = db.Column(db.Float, nullable=False)
    shipping_discount = db.Column(db.Float, nullable=False)

    @classmethod
    def from_json(cls, promotion_json, user, create_products=False):
        product_ids = set(map(lambda prom: prom.get('product_id'),
                              promotion_json))
        products = {
            p.id: p
            for p in Product.query.filter(Product.id.in_(product_ids))
        }

        ret = []

        for promotion in promotion_json:
            product = products.get(promotion['product_id'])
            if not product:
                product_id = promotion['product_id']
                if not create_products:
                    raise NotFoundError(
                        'Product {} not found'.format(product_id),
                        payload={'id': product_id})

                product = Product(id=product_id,
                                  user_id=user.id,
                                  name=promotion['product_name'],
                                  description=promotion['product_description'],
                                  price=promotion['price'])
                db.session.add(product)
                products[product.id] = product

            if product.user_id != user.id:
                raise ForbiddenError('Forbidden', payload={
                    'error': 'User cannot create discounts for these products.'
                })

            promotion_obj = cls(**promotion)
            ret.append(promotion_obj)

        if ret:
            db.session.add_all(ret)
            db.session.commit()

        return ret
