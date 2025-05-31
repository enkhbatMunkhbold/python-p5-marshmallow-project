from marshmallow import fields, validate, ValidationError
from flask import request, session, jsonify, make_response
from flask_restful import Resource

# Local imports
from config import app, db, api, ma
# Add your model imports


# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


if __name__ == '__main__':
    app.run(port=5555, debug=True)

