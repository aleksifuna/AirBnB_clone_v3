#!/usr/bin/python3
"""view for amenities object that handles all default RESTFul API actions"""
from . import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Returns a list of all amenity objects"""
    amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_list)


@app_views.route(
        '/amenities/<amenity_id>',
        methods=['GET'],
        strict_slashes=False
        )
def get_amenity(amenity_id):
    """Return a dict representation of amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)


@app_views.route(
        '/amenities/<amenity_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_amenity(amenity_id):
    """Deletes a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        '/amenities/',
        methods=['POST'],
        strict_slashes=False
        )
def create_amenity():
    """Creates an Amenity object"""
    if request.get_json():
        if 'name' not in request.get_json():
            return jsonify({"error": "Missing name"}), 400
        data = request.get_json()
        amenity = Amenity(**data)
        amenity.save()
        return amenity.to_dict(), 201
    else:
        return jsonify({"error": "Not a JSON"}), 400


@app_views.route(
        '/amenities/<amenity_id>',
        methods=['PUT'],
        strict_slashes=False
        )
def update_amenity(amenity_id):
    """updates amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if request.get_json():
            for key, value in request.get_json().items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(amenity, key, value)
            amenity.save()
            return amenity.to_dict(), 200
        else:
            return jsonify({"error": "Not a JSON"}), 400
    else:
        abort(404)
