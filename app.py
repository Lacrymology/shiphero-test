from flask import Flask, jsonify

from exceptions import HttpError

app = Flask('shiphero')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

@app.errorhandler(HttpError)
def handle_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
