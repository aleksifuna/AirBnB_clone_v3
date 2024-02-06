#!/usr/bin/python3
"""view for city object that handles all default RESTFul API actions"""
from . import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Returns a list of all states objects"""
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route(
        '/states/<state_id>',
        methods=['GET'],
        strict_slashes=False
        )
def get_state(state_id):
    """Return a dict representation of state object"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict()), 200
    else:
        abort(404)


@app_views.route(
        '/states/<state_id>',
        methods=['DELETE'],
        strict_slashes=False
        )
def delete_state(state_id):
    """Delete a state object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        '/states/',
        methods=['POST'],
        strict_slashes=False
        )
def create_state():
    """Creates a state object"""
    if request.get_json():
        if 'name' not in request.get_json():
            return jsonify({"error": "Missing name"}), 400
        data = request.get_json()
        state = State(**data)
        state.save()
        return state.to_dict(), 201
    else:
        return jsonify({"error": "Not a JSON"}), 400


@app_views.route(
        '/states/<state_id>',
        methods=['PUT'],
        strict_slashes=False
        )
def update_state(state_id):
    """updates state object"""
    state = storage.get(State, state_id)
    if state:
        if request.get_json():
            for key, value in request.get_json().items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(state, key, value)
            return state.to_dict(), 200
        else:
            return jsonify({"error": "Not a JSON"}), 400
    else:
        abort(404)
