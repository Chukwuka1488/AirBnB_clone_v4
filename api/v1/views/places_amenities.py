#!/usr/bin/python3
"""
This module contains the Flask routes for the link between 'Place' and 'Amenity' objects and the 
HTTP methods to handle them. It handles the following routes:

- GET /api/v1/places/<place_id>/amenities
- DELETE /api/v1/places/<place_id>/amenities/<amenity_id>
- POST /api/v1/places/<place_id>/amenities/<amenity_id>
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity

@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """ Retrieves the list of all Amenity objects of a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = place.amenities if type(place.amenities) == list else place.amenities()
    return jsonify([amenity.to_dict() for amenity in amenities])

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """ Deletes a Amenity object to a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    if type(place.amenities) == list:
        place.amenities.remove(amenity)
    else:
        place.amenities().remove(amenity)
    place.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """ Link a Amenity object to a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    if type(place.amenities) == list:
        place.amenities.append(amenity)
    else:
        place.amenities().append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
