#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions
"""

from . import app_views
from models.base_model import BaseModel
from flask import Flask, abort, request, make_response
from models.state import Amenity
from models import storage


@app_views.route('/amenities/', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route(
        '/amenities/<amenity_id>',
        methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False
        )
def states(amenity_id=None):
    """ get state objects with or with id"""

    if amenity_id:
        amenities = storage.get(Amenity, amenity_id)

        if request.method == 'PUT':
            if amenities:
                data = request.get_json()
                if data:
                    amenities.name = data['name']
                    storage.new(amenities)
                    storage.save()
                    return make_response(amenities.to_dict(), 200)
                else:
                    return make_respose("Not a JSON", 404)
            else:
                abort(404)

        if request.method == 'DELETE':
            if amenities:

                storage.delete(amenities)
                storage.save()

                return make_response({}, 200)
            else:
                abort(404)

        if amenities:
            return amenities.to_dict()
        else:
            abort(404)
    else:
        if request.method == "POST":
            data = request.get_json()
            if data:
                if "name" not in data.keys():
                    return make_respose("Missing name", 404)

                amenities = Amenity(name=data['name'])
                storage.new(amenities)
                storage.save()
                return make_response(amenities.to_dict(), 201)

            else:
                return make_respose("Not a JSON", 404)

        # get all states
        amenities_obj = storage.all(Amenity)

        obj_list = []
        for obj in amenities_obj.values():
            obj_list.append(obj.to_dict())

        return obj_list
