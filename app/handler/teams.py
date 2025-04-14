from flask import jsonify
from app.dao.teams import TeamsDAO
from app.handler.handler_analytics import AnalyticsHandler

class TeamHandler:
    
    def insertTeam(self,json):
        if 'name' not in json or 'sport_id' not in json:
            return jsonify({"error": "Missing parameters"}), 400
        
        name = json['name']
        sport = json['sport_id']

        
        dao = TeamsDAO()
        
        if not dao.sportExists(sport):
            return jsonify({"error": "Sport ID not found"}), 404
        
        id = dao.insertTeam(sport, name)
        json["id"] = id
        return jsonify({"team_id": id, "name": name, "sport_id": sport}), 201
    
    def getAllTeams(self):
        dao = TeamsDAO()
        teams = dao.getAllTeams()
        return jsonify(teams), 200
    
    def getTeamByID(self, id):
        dao = TeamsDAO()
        team = dao.getTeamByID(id)
        
        if not team:
            return jsonify({"error": "Team ID not found"}), 404
        
        return jsonify(team), 200
    
    def updateTeam(self, id, json):
        if 'name' not in json or ('sport_id' not in json and 'sport' not in json):
            return jsonify({"error": "Missing parameters"}), 400
        name = json['name']
        sport = json.get('sport_id') or json.get('sport')
         
        dao = TeamsDAO()
        if not dao.teamExists(id):
            return jsonify({"error": "Team ID not found"}), 404
        if not dao.sportExists(sport):
            return jsonify({"error": "Sport ID not found"}), 404
        result = dao.updateTeam(id, name, sport)
        if(result):
            return jsonify({"team_id": id, "name": name, "sport": sport}), 200
        else:
            return jsonify({"error": "Failed to update team"}), 500
        
    def deleteTeam(self, id):
        dao = TeamsDAO()
        
        if not dao.teamExists(id):
            return jsonify({"error": "Team ID not found"}), 404
        
        if dao.teamReferences(id):
            return jsonify({"error": "Attempting to delete referenced records"}), 409
        
        dao.deleteTeam(id)
        return '', 204

    def getTopTeams(self):
        return AnalyticsHandler().getTopTeams()

    def getSportsDistribution(self):
        return AnalyticsHandler().getSportsDistribution()
