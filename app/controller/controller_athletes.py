from flask import Blueprint, request, jsonify
from app.handler.handler_athlete import AthleteHandler

athlete_routes = Blueprint("athlete_routes", __name__)
handler = AthleteHandler()

@athlete_routes.route("/athlete", methods=["GET"])
def get_all_athletes():
    return jsonify(handler.get_all_athletes()), 200

@athlete_routes.route("/athlete/<int:athlete_id>", methods=["GET"])
def get_athlete(athlete_id):
    result = handler.get_athlete_by_id(athlete_id)
    return jsonify(result[0]), result[1] if isinstance(result, tuple) else 200

@athlete_routes.route("/athlete", methods=["POST"])
def create_athlete():
    data = request.json
    result = handler.insert_athlete(data)
    return jsonify(result[0]), result[1] if isinstance(result, tuple) else 201

@athlete_routes.route("/athlete/<int:athlete_id>", methods=["PUT"])
def update_athlete(athlete_id):
    data = request.json
    result = handler.update_athlete(athlete_id, data)
    return jsonify(result[0]), result[1] if isinstance(result, tuple) else 200

@athlete_routes.route("/athlete/<int:athlete_id>", methods=["DELETE"])
def delete_athlete(athlete_id):
    result = handler.delete_athlete(athlete_id)
    return jsonify(result[0]), result[1] if isinstance(result, tuple) else 204
