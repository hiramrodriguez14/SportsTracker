from flask import jsonify
from app.dao.dao_sport import SportDAO

class SportHandler:
    def __init__(self):
        self.dao = SportDAO()

    def getAllSports(self):
        result = self.dao.getAllSports()
        mapped = [{"id": r[0], "name": r[1], "gender": r[2], "venue": r[3]} for r in result]
        return jsonify(mapped)

    def getSportById(self, sport_id):
        result = self.dao.getSportByIdWithExercises(sport_id)
        if result:
            return jsonify(result)
        return jsonify({"Error": "Sport Not Found"}), 404

    def insertSport(self, json):
        name = json.get("name")
        gender = json.get("gender")
        venue = json.get("venue")
        if name and gender and venue:
            sport_id = self.dao.insertSport(name, gender, venue)
            return jsonify({"id": sport_id, "name": name, "gender": gender, "venue": venue}), 201
        return jsonify({"Error": "Missing fields"}), 400

    def updateSport(self, sport_id, json):
        name = json.get("name")
        gender = json.get("gender")
        venue = json.get("venue")
        if name and gender and venue:
            self.dao.updateSport(sport_id, name, gender, venue)
            return jsonify({"id": sport_id, "name": name, "gender": gender, "venue": venue})
        return jsonify({"Error": "Missing fields"}), 400

    def deleteSport(self, sport_id):
        self.dao.deleteSport(sport_id)
        return ("", 204)