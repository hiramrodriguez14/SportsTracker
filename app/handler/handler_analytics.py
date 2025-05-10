from flask import jsonify
from app.model.dao.dao_analytics import AnalyticsDAO

class AnalyticsHandler:
    def __init__(self):
        self.dao = AnalyticsDAO()

    def getTopTeams(self, jsonify_result=True):
        data = self.dao.getTopTeams()
        result = []
        for row in data:
            result.append({
                "team_id": row[0],
                "name": row[1],
                "sport": row[2],
                "championships_won": row[3]
            })

        if jsonify_result:
            return jsonify(result)
        else:
            return result
    

    def getSportsDistribution(self, jsonify_result=True):
        data = self.dao.getSportsDistribution()
        result = []
        for row in data:
            result.append({
                "sport": row[0],
                "team_count": row[1]
            })
            
        if jsonify_result:
            return jsonify(result)
        else:
            return result

    def getMostChampionshipWins(self, jsonify_result=True):
        data = self.dao.getMostChampionshipWins()
        result = []
        for row in data:
            result.append({
                "team_id": row[0],
                "name": row[1],
                "total_wins": row[2]
            })
        if jsonify_result:
            return jsonify(result)
        else:
            return result

    def getSportPopularity(self, jsonify_result=True):
        data = self.dao.getSportPopularity()
        result = []
        for row in data:
            result.append({
                "sport": row[0],
                "athlete_count": row[1]
            })
        if jsonify_result:
            return jsonify(result)
        else:
            return result
