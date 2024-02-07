#!/usr/bin/python3
"""view for link between place/amenity that handles
all default RESTFul API actions"""
from . import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from models import storage_t


@app_views.route(
        '/places/<place_id>/amenities',
        methods=['GET'],
        strict_slashes=False
        )
def get_place_amenites(place_id):
    """Returns a list of all amenity of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenites), 200


@app_views.route(
        'places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def remove_amenity(place_id, amenity_id):
    """removes and amenity from place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    if storage_t == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity.id)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['POST'],
        strict_slashes=False
        )
def link_amenity(place_id, amenity_id):
    """Creates amenity to a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    if storage_t == "db":
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity.id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
