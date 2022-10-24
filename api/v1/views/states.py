#!/usr/bin/python3
"""handles all default RESTFul API actions for `State` objects"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states/", strict_slashes=False, methods=["GET"])
def all_states():
    """retrieves all state objects"""
    states = []
    for obj in storage.all().values():
        if obj.to_dict()["__class__"] == "State":
            states.append(obj.to_dict())
    return jsonify(states)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def get_state_object(state_id):
    """retrieves a state object based on the `state_id`"""
    if storage.get(State, state_id) is None:
        abort(404)
    return jsonify(storage.get(State, state_id).to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_state_object(state_id):
    """retrieves a state object based on the `state_id`"""
    if storage.get(State, state_id) is None:
        abort(404)
    obj_id = "State." + state_id
    if storage.all()[obj_id] is not None:
        del storage.all()[obj_id]
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state_object():
    """creates a new state object"""
    if not request.is_json:
        return make_response(jsonify({"error", "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error", "Missing name"}), 400)
    new_state = State()
    new_state.name = request.get_json()["name"]
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state_object(state_id):
    """updates a state object"""
    if storage.get(State, state_id) is None:
        abort(404)
    if not request.is_json:
        return make_response(jsonify({"error", "Not a JSON"}), 400)
    state = storage.get(State, state_id)
    for key, value in request.get_json().items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
