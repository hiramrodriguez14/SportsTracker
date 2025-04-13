from flask import Flask, request
from handler.handler_sport import SportHandler
from handler.handler_championship import ChampionshipHandler
from handler.handler_analytics import AnalyticsHandler

app = Flask(__name__)

@app.route("/sport", methods=["GET"])
def getAllSports():
    return SportHandler().getAllSports()

@app.route("/sport/<int:sport_id>", methods=["GET"])
def getSportById(sport_id):
    return SportHandler().getSportById(sport_id)

@app.route("/sport", methods=["POST"])
def insertSport():
    return SportHandler().insertSport(request.json)

@app.route("/sport/<int:sport_id>", methods=["PUT"])
def updateSport(sport_id):
    return SportHandler().updateSport(sport_id, request.json)

@app.route("/sport/<int:sport_id>", methods=["DELETE"])
def deleteSport(sport_id):
    return SportHandler().deleteSport(sport_id)

@app.route("/championship", methods=["GET"])
def getAllChampionships():
    return ChampionshipHandler().getAllChampionships()

@app.route("/championship/<int:champ_id>", methods=["GET"])
def getChampionshipById(champ_id):
    return ChampionshipHandler().getChampionshipById(champ_id)

@app.route("/championship", methods=["POST"])
def insertChampionship():
    return ChampionshipHandler().insertChampionship(request.json)

@app.route("/championship/<int:champ_id>", methods=["PUT"])
def updateChampionship(champ_id):
    return ChampionshipHandler().updateChampionship(champ_id, request.json)

@app.route("/championship/<int:champ_id>", methods=["DELETE"])
def deleteChampionship(champ_id):
    return ChampionshipHandler().deleteChampionship(champ_id)

@app.route("/teams/top-teams", methods=["GET"])
def getTopTeams():
    return AnalyticsHandler().getTopTeams()

@app.route("/teams/sports-distribution", methods=["GET"])
def getSportsDistribution():
    return AnalyticsHandler().getSportsDistribution()

@app.route("/championships/most-wins", methods=["GET"])
def getMostChampionshipWins():
    return AnalyticsHandler().getMostChampionshipWins()

@app.route("/sports/popularity", methods=["GET"])
def getSportPopularity():
    return AnalyticsHandler().getSportPopularity()
