from flask import jsonify
from app.dao.dao_championship import ChampionshipDAO

class ChampionshipHandler:
    def __init__(self):
        self.dao = ChampionshipDAO()

    def getAllChampionships(self):
        result = self.dao.getAllChampionships()
        mapped = [{"id": r[0], "name": r[1], "year": r[2], "winner_team_id": r[3]} for r in result]
        return jsonify(mapped)

    def getChampionshipById(self, champ_id):
        result = self.dao.getChampionshipByIdWithWinner(champ_id)
        if result:
            return jsonify(result)
        return jsonify({"Error": "Championship Not Found"}), 404

    def insertChampionship(self, json):
        name = json.get("name")
        year = json.get("year")
        winner_team_id = json.get("winner_team_id")
        if name and year and winner_team_id:
            champ_id = self.dao.insertChampionship(name, year, winner_team_id)
            return jsonify({"id": champ_id, "name": name, "year": year, "winner_team_id": winner_team_id}), 201
        return jsonify({"Error": "Missing fields"}), 400

    def updateChampionship(self, champ_id, json):
        name = json.get("name")
        year = json.get("year")
        winner_team_id = json.get("winner_team_id")
        if name and year and winner_team_id:
            self.dao.updateChampionship(champ_id, name, year, winner_team_id)
            return jsonify({"id": champ_id, "name": name, "year": year, "winner_team_id": winner_team_id})
        return jsonify({"Error": "Missing fields"}), 400

    def deleteChampionship(self, champ_id):
        self.dao.deleteChampionship(champ_id)
        return ("", 204)
