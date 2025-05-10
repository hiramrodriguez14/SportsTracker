from flask import Blueprint, request, jsonify
from app.handler.teams import TeamHandler

team_routes = Blueprint("team_routes", __name__)
handler = TeamHandler()

@team_routes.route("/team", methods=["GET"])
def get_all_teams():
    return jsonify(handler.get_all_teams()), 200

@team_routes.route("/team/<int:team_id>", methods=["GET"])
def get_team(team_id):
    result = handler.get_team_by_id(team_id)
    return jsonify(result[0]), result[1] if isinstance(result, tuple) else 200

@team_routes.route("/team", methods=["POST"])
def create_team():
    data = request.json
    result = handler.insert_team(data)
    return jsonify(result[0]), result[1] if isinstance(result, tuple) else 201

@team_routes.route("/team/<int:team_id>", methods=["PUT"])
def update_team(team_id):
    data = request.json
    result = handler.update_team(team_id, data)
    return jsonify(result[0]), result[1] if isinstance(result, tuple) else 200

@team_routes.route("/team/<int:team_id>", methods=["DELETE"])
def delete_team(team_id):
    result = handler.delete_team(team_id)
    return jsonify(result[0]), result[1] if isinstance(result, tuple) else 204
