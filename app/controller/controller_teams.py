from flask import Blueprint, request, jsonify
from app.handler.teams import TeamHandler

team_routes = Blueprint("team_routes", __name__)
handler = TeamHandler()

@team_routes.route("/team", methods=["GET"])
def get_all_teams():
    return handler.getAllTeams()

@team_routes.route("/team/<int:team_id>", methods=["GET"])
def get_team(team_id):
    return handler.getTeamByID(team_id)
     

@team_routes.route("/team", methods=["POST"])
def create_team():
    data = request.json
    return handler.insertTeam(data)
   
@team_routes.route("/team/<int:team_id>", methods=["PUT"])
def update_team(team_id):
    data = request.json
    return handler.updateTeam(team_id, data)
   

@team_routes.route("/team/<int:team_id>", methods=["DELETE"])
def delete_team(team_id):
    return handler.deleteTeam(team_id)
   
