from flask import request, jsonify

from exceptions import HttpError
from app import app
from inputs import parse
from models import Product, Promotion
from utils import authenticate

# NOTE: generally, I'd rather lean towards using class-based views rather than
#  functions, and since I'm designing this as a REST API, I'd have some helpers
#  to automatize calls to jsonify and setting status codes and such, and I'd
#  also define a set of Exception subclasses to be handled as HTTP error
#  status responses

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
