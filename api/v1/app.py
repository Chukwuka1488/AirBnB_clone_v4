#!/usr/bin/python3
"""
Flask API Setup
"""

from flask import Flask, jsonify, make_response, Blueprint
from models import storage
from models.engine import *
from api.v1.views import app_views
from os import getenv


""" Flask instances """
app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_close(error):
    """ Close file and delete database """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ function to handle error 404 """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0,0,0,0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True, debug=True)
