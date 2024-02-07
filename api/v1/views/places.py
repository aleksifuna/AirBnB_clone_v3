#!/usr/bin/python3
"""view for place object that handles all default RESTFul API actions"""
from . import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
        '/cities/<city_id>/places',
        methods=['GET'],
        strict_slashes=False
        )
def get_place_city(city_id):
    """Returns a list of all place objects of in a city"""
    city = storage.get(City, city_id)
    if city:
        places = [place.to_dict() for place in city.places]
        return jsonify(places), 200
    else:
        abort(404)


@app_views.route(
        '/places/<place_id>',
        methods=['GET'],
        strict_slashes=False)
def get_place(place_id):
    """Return a dict representation of place object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict()), 200
    else:
        abort(404)


@app_views.route(
        '/places/<place_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_place(place_id):
    """Delete a place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        '/cities/<city_id>/places',
        methods=['POST'],
        strict_slashes=False
        )
def create_place(city_id):
    """Creates a place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing name")
    if storage.get(User, data['user_id']) is None:
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return place.to_dict(), 201


@app_views.route(
        '/places/<place_id>',
        methods=['PUT'],
        strict_slashes=False
        )
def update_place(place_id):
    """updates place object"""
    place = storage.get(Place, place_id)
    ignore_list = ['id', 'state_id', 'created_at', 'updated_at']
    if place:
        if request.get_json():
            for key, value in request.get_json().items():
                if key not in ignore_list:
                    setattr(place, key, value)
            place.save()
            return place.to_dict(), 200
        else:
            return abort(400, "Not a JSON")
    else:
        abort(404)
