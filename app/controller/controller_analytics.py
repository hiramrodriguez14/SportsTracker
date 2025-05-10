from flask import Blueprint, request
from app.handler.handler_sport import SportHandler
from app.handler.handler_championship import ChampionshipHandler
from app.handler.handler_analytics import AnalyticsHandler

analytics_routes = Blueprint("analytics_routes", __name__)
sport_handler = SportHandler()
champ_handler = ChampionshipHandler()
analytics_handler = AnalyticsHandler()

@analytics_routes.route("/sport", methods=["GET"])
def get_all_sports():
    return sport_handler.getAllSports()

@analytics_routes.route("/sport/<int:sport_id>", methods=["GET"])
def get_sport_by_id(sport_id):
    return sport_handler.getSportById(sport_id)

@analytics_routes.route("/sport", methods=["POST"])
def insert_sport():
    return sport_handler.insertSport(request.json)

@analytics_routes.route("/sport/<int:sport_id>", methods=["PUT"])
def update_sport(sport_id):
    return sport_handler.updateSport(sport_id, request.json)

@analytics_routes.route("/sport/<int:sport_id>", methods=["DELETE"])
def delete_sport(sport_id):
    return sport_handler.deleteSport(sport_id)

@analytics_routes.route("/championship", methods=["GET"])
def get_all_championships():
    return champ_handler.getAllChampionships()

@analytics_routes.route("/championship/<int:champ_id>", methods=["GET"])
def get_championship_by_id(champ_id):
    return champ_handler.getChampionshipById(champ_id)

@analytics_routes.route("/championship", methods=["POST"])
def insert_championship():
    return champ_handler.insertChampionship(request.json)

@analytics_routes.route("/championship/<int:champ_id>", methods=["PUT"])
def update_championship(champ_id):
    return champ_handler.updateChampionship(champ_id, request.json)

@analytics_routes.route("/championship/<int:champ_id>", methods=["DELETE"])
def delete_championship(champ_id):
    return champ_handler.deleteChampionship(champ_id)

@analytics_routes.route("/teams/top-teams", methods=["GET"])
def get_top_teams():
    return analytics_handler.getTopTeams()

@analytics_routes.route("/teams/sports-distribution", methods=["GET"])
def get_sports_distribution():
    return analytics_handler.getSportsDistribution()

@analytics_routes.route("/championships/most-wins", methods=["GET"])
def get_most_championship_wins():
    return analytics_handler.getMostChampionshipWins()

@analytics_routes.route("/sports/popularity", methods=["GET"])
def get_sport_popularity():
    return analytics_handler.getSportPopularity()
