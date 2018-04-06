from flask import request, jsonify

from exceptions import HttpError
from app import app
from inputs import parse
from models import Product, Promotion

# NOTE: generally, I'd rather lean towards using class-based views rather than
#  functions, and since I'm designing this as a REST API, I'd have some helpers
#  to automatize calls to jsonify and setting status codes and such, and I'd
#  also define a set of Exception subclasses to be handled as HTTP error
#  status responses

@app.route('/discounts/add', methods=['POST'])
def add_discounts():
    discounts = request.files.get('discounts')
    if not discounts or not discounts.filename:
        raise HttpError('Missing field', 400, {
            'errors': {
                'discounts': 'this field is required',
            },
        })

    discounts_json = parse(discounts)

    return jsonify(discounts_json)
