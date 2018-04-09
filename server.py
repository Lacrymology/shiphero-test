from flask import request, jsonify

from exceptions import HttpError
from app import app
from inputs import parse
from models import Product, Promotion
from utils import authenticate

# I assumed that since the discounts input came with the product name,
# description and price, these may represent a change in those fields which is
# only valid for the time the discount is up. For simplicity, when the
# Promotion object is created, these fields are loaded from the product
# object, but I understand this may not be the best pattern depending on the
# use-case, because any later changes on the product would not be reflected.
# Overriding empty fields in the Promotion object with their Product
# counterpart if they're empty on the view/serializing function would be
# a better approach. I'd need to understand the reason behind these fields
# being sent in the promotion datasheets better to decide whether the best
# course of action would be overriding the Product fields with them, rather
# than this redundancy.

# NOTE: generally, I'd rather lean towards using class-based views rather than
#  functions, and since I'm designing this as a REST API, I'd have some helpers
#  to automatize calls to jsonify and setting status codes and such.

@app.route('/promotions/add', methods=['POST'])
@authenticate
def add_promotions():
    promotions_file = request.files.get('promotions')
    if not promotions_file or not promotions_file.filename:
        raise HttpError('Missing field', 400, {
            'errors': {
                'discounts': 'this field is required',
            },
        })

    promotions_parsed = parse(promotions_file)

    # for production, create_products should probably be 'false'. I set it
    #  as a facility to automatically create missing products
    promotions = Promotion.from_file(promotions_parsed, request.user,
                                     create_products=True)
    promotions_dict = list(map(serialize_promotion, promotions))

    response = jsonify(promotions_dict)
    response.status_code = 201
    return response


@app.route('/promotions', methods=['GET'])
@authenticate
def list_promotions():
    """
    Returns the user's promotions
    """
    promotions = Promotion.query.join(Product).filter(
        Product.user==request.user)
    promotions_dict = list(map(serialize_promotion, promotions))
    return jsonify(promotions_dict)


def serialize_promotion(promotion):
    """
    Turns a Promotion object into a dict for jsonification
    """
    return {
        'id': promotion.id,
        'product_id': promotion.product_id,
        'product_name': promotion.product_name,
        'product_description': promotion.product_description,
        'price': promotion.price,
        'discount': promotion.discount,
        'final_price': round(promotion.price * (1 - promotion.discount), 2),
        'shipping_discount': promotion.shipping_discount,
    }
