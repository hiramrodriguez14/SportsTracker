from flask import Blueprint, request, jsonify
from app.handler.teams import TeamHandler

team_routes = Blueprint("team_routes", __name__)
handler = TeamHandler()

@team_routes.route("/team", methods=["GET"])
def get_all_teams():
    return jsonify(handler.getAllTeams()), 200

@team_routes.route("/team/<int:team_id>", methods=["GET"])
def get_team(team_id):
    result = handler.getTeamByID(team_id)
    return jsonify(result[0]), result[1] if isinstance(result, tuple) else 200

@team_routes.route("/team", methods=["POST"])
def create_team():
    data = request.json
    result = handler.insertTeam(data)
    return jsonify(result[0]), result[1] if isinstance(result, tuple) else 201

@team_routes.route("/team/<int:team_id>", methods=["PUT"])
def update_team(team_id):
    data = request.json
    result = handler.updateTeam(team_id, data)
    return jsonify(result[0]), result[1] if isinstance(result, tuple) else 200

@team_routes.route("/team/<int:team_id>", methods=["DELETE"])
def delete_team(team_id):
    result = handler.deleteTeam(team_id)
    return jsonify(result[0]), result[1] if isinstance(result, tuple) else 204
