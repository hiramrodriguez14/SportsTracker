from flask import jsonify
from app.dao.dao_analytics import AnalyticsDAO

class AnalyticsHandler:
    def __init__(self):
        self.dao = AnalyticsDAO()

    def getTopTeams(self):
        data = self.dao.getTopTeams()
        result = []
        for row in data:
            result.append({
                "team_id": row[0],
                "name": row[1],
                "sport": row[2],
                "championships_won": row[3]
            })
        return jsonify(result)

    def getSportsDistribution(self):
        data = self.dao.getSportsDistribution()
        result = []
        for row in data:
            result.append({
                "sport": row[0],
                "team_count": row[1]
            })
        return jsonify(result)

    def getMostChampionshipWins(self):
        data = self.dao.getMostChampionshipWins()
        result = []
        for row in data:
            result.append({
                "team_id": row[0],
                "name": row[1],
                "total_wins": row[2]
            })
        return jsonify(result)

    def getSportPopularity(self):
        data = self.dao.getSportPopularity()
        result = []
        for row in data:
            result.append({
                "sport": row[0],
                "athlete_count": row[1]
            })
        return jsonify(result)
