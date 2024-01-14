#!/usr/bin/python3
"""Flask app to generate complete html page containing location/amenity
dropdown menus and rental listings"""
from flask import Flask, render_template, url_for
from models import storage
import uuid

app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'

@app.route('/0-hbnb')
def hbnb_filters(the_id=None):
    """
    handles requests to custom template with, cities and amenities
    """
    state_objs = storage.all('State').values()
    states = dict([state.name, state] for state in state_objs)
    amens = storage.all('Amenity').values()
    places = storage.all('Place').values()
    users = dict([user.id, "{} {}".format(user.first_name, user.last_name)]
            for user in storage.all('User').values())
    return render_template('0-hbnb.html', 
            states=states, 
            amens=amens, 
            places=places, 
            users=users, 
            cache_id=uuid.uuid4())


@app.teardown_appcontext
def teardown_db(*args, **kwargs):
    """Close database or file storage"""
    storage.close()


if __name__ == '__main__':
    app.run(host=host, port=port)
