#!/usr/bin/python3
"""
a new view for State objects that handles all default RESTFul API actions
"""

from . import app_views
from models.base_model import BaseModel
from flask import Flask, abort, request, make_response, jsonify
from models.state import State
from models import storage


@app_views.route('/states/', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route(
        '/states/<state_id>',
        methods=['GET', 'DELETE', 'PUT'],
        strict_slashes=False
        )
def states(state_id=None):
    """ get state objects with or with id"""

    if state_id:
        state = storage.get(State, state_id)

        if request.method == 'PUT':
            if state:
                data = request.get_json()
                if data:
                    state.name = data['name']
                    storage.new(state)
                    storage.save()
                    return make_response(state.to_dict(), 200)
                else:
                    return make_respose("Not a JSON", 404)
            else:
                abort(404)

        if request.method == 'DELETE':
            if state:
                if state.cities:
                    for city in state.cities:
                        storage.delete(city)

                storage.delete(state)
                storage.save()

                return make_response({}, 200)
            else:
                abort(404)

        if state:
            return state.to_dict()
        else:
            abort(404)
    else:
        if request.method == "POST":
            data = request.get_json()
            if data:
                if "name" not in data.keys():
                    return make_respose("Missing name", 404)

                state = State(name=data['name'])
                storage.new(state)
                storage.save()
                return make_response(state.to_dict(), 201)

            else:
                return make_respose("Not a JSON", 404)

        # get all states
        state_obj = storage.all(State)

        obj_list = []
        for obj in state_obj.values():
            obj_list.append(obj.to_dict())

        return jsonify(obj_list)
