from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Import handlers
from app.handler.athletes import AthleteHandler
from app.handler.exercise_instructions import ExerciseInstructionsHandler
from app.handler.teams import TeamHandler
from app.handler.exercise_image import ExerciseImageHandler
from app.handler.exercise_primary_muscles import ExercisePrimaryMusclesHandler
from app.handler.exercise_secondary_muscles import ExerciseSecondaryMusclesHandler
from app.handler.sport_exercises import SportExercisesHandler
from app.handler.exercise import ExerciseHandler
from app.handler.handler_sport import SportHandler
from app.handler.handler_championship import ChampionshipHandler
from app.handler.handler_analytics import AnalyticsHandler

# Trigger DB selector
from bug_handling.choose_db import get_db_config
_ = get_db_config()


# Flask setup
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "🏃‍♂️ Welcome to the SportsTracker API for DB team PHGA. Keep doing your thing on Postman."

# ATHLETE ROUTES
athlete_handler = AthleteHandler()

@app.route("/athlete", methods=["GET"])
def get_all_athletes():
    return jsonify(athlete_handler.get_all_athletes()), 200

@app.route("/athlete/<int:athlete_id>", methods=["GET"])
def get_athlete_by_id(athlete_id):
    return jsonify(athlete_handler.get_athlete_by_id(athlete_id)), 200

@app.route("/athlete", methods=["POST"])
def create_athlete():
    return jsonify(athlete_handler.insert_athlete(request.json)[0]), 201

@app.route("/athlete/<int:athlete_id>", methods=["PUT"])
def update_athlete(athlete_id):
    return jsonify(athlete_handler.update_athlete(athlete_id, request.json)[0]), 200

@app.route("/athlete/<int:athlete_id>", methods=["DELETE"])
def delete_athlete(athlete_id):
    return jsonify(athlete_handler.delete_athlete(athlete_id)[0]), 204

# TEAM ROUTES
team_handler = TeamHandler()

@app.route("/team", methods=["GET"])
def get_all_teams():
    return team_handler.getAllTeams()

@app.route("/team/<int:team_id>", methods=["GET"])
def get_team_by_id(team_id):
    return team_handler.getTeamByID(team_id)

@app.route("/team", methods=["POST"])
def create_team():
    return team_handler.insertTeam(request.json)

@app.route("/team/<int:team_id>", methods=["PUT"])
def update_team(team_id):
    return team_handler.updateTeam(team_id, request.json)

@app.route("/team/<int:team_id>", methods=["DELETE"])
def delete_team(team_id):
    return team_handler.deleteTeam(team_id)

@app.route("/teams/top-teams", methods=["GET"])
def get_top_teams():
    return team_handler.getTopTeams()

@app.route("/teams/sports-distribution", methods=["GET"])
def get_sports_distribution():
    return team_handler.getSportsDistribution()

# EXERCISE ROUTES
exercise_handler = ExerciseHandler()

@app.route("/exercise", methods=["POST"])
def create_exercise():
    return exercise_handler.create_exercise(request.json)

@app.route("/exercise", methods=["GET"])
def get_all_exercises():
    return exercise_handler.get_all_exercises()

@app.route("/exercise/<int:exercise_id>", methods=["GET", "PUT", "DELETE"])
def exercise_crud(exercise_id):
    if request.method == "GET":
        return exercise_handler.get_exercise(exercise_id)
    elif request.method == "PUT":
        return exercise_handler.update_exercise(exercise_id, request.json)
    elif request.method == "DELETE":
        return exercise_handler.delete_exercise(exercise_id)

@app.route("/exercises/most-performed", methods=["GET"])
def get_most_performed_exercises():
    return exercise_handler.get_most_performed_exercises()

@app.route("/exercises/muscle-group", methods=["GET"])
def get_exercises_by_muscle():
    muscle = request.args.get("muscle")
    if not muscle:
        return jsonify({"error": "Missing 'muscle' parameter"}), 400
    return exercise_handler.get_exercises_by_muscle(muscle)

@app.route("/exercises/most-complex", methods=["GET"])
def get_most_complex_exercises():
    return exercise_handler.get_most_complex_exercises()

# SPORT ROUTES
sport_handler = SportHandler()

@app.route("/sport", methods=["GET"])
def get_all_sports():
    return sport_handler.getAllSports()

@app.route("/sport/<int:sport_id>", methods=["GET"])
def get_sport_by_id(sport_id):
    return sport_handler.getSportById(sport_id)

@app.route("/sport", methods=["POST"])
def insert_sport():
    return sport_handler.insertSport(request.json)

@app.route("/sport/<int:sport_id>", methods=["PUT"])
def update_sport(sport_id):
    return sport_handler.updateSport(sport_id, request.json)

@app.route("/sport/<int:sport_id>", methods=["DELETE"])
def delete_sport(sport_id):
    return sport_handler.deleteSport(sport_id)


# CHAMPIONSHIP ROUTES
championship_handler = ChampionshipHandler()

@app.route("/championship", methods=["GET"])
def get_all_championships():
    return championship_handler.getAllChampionships()

@app.route("/championship/<int:champ_id>", methods=["GET"])
def get_championship_by_id(champ_id):
    return championship_handler.getChampionshipById(champ_id)

@app.route("/championship", methods=["POST"])
def insert_championship():
    return championship_handler.insertChampionship(request.json)

@app.route("/championship/<int:champ_id>", methods=["PUT"])
def update_championship(champ_id):
    return championship_handler.updateChampionship(champ_id, request.json)

@app.route("/championship/<int:champ_id>", methods=["DELETE"])
def delete_championship(champ_id):
    return championship_handler.deleteChampionship(champ_id)


# ANALYTICS ROUTES
analytics_handler = AnalyticsHandler()

@app.route("/championships/most-wins", methods=["GET"])
def get_most_championship_wins():
    return analytics_handler.getMostChampionshipWins()

@app.route("/sports/popularity", methods=["GET"])
def get_sport_popularity():
    return analytics_handler.getSportPopularity()


# RELATIONSHIP ROUTES
@app.route('/exercise/<int:exercise_id>/instruction', methods=['POST'])
def add_exercise_instruction(exercise_id):
    return ExerciseInstructionsHandler().insertExerciseInstruction(exercise_id, request.json)

@app.route('/exercise/<int:exercise_id>/instruction/<int:instruction_id>', methods=['DELETE'])
def delete_exercise_instruction(exercise_id, instruction_id):
    return ExerciseInstructionsHandler().deleteExerciseInstruction(exercise_id, instruction_id)

@app.route('/exercise/<int:exercise_id>/image', methods=['POST'])
def add_exercise_image(exercise_id):
    return ExerciseImageHandler().insertExerciseImage(exercise_id, request.json)

@app.route('/exercise/<int:exercise_id>/image/<int:image_id>', methods=['DELETE'])
def delete_exercise_image(exercise_id, image_id):
    return ExerciseImageHandler().deleteExerciseImage(exercise_id, image_id)

@app.route('/exercise/<int:exercise_id>/primary-muscle', methods=['POST'])
def add_primary_muscle(exercise_id):
    return ExercisePrimaryMusclesHandler().insertExercisePrimaryMuscle(exercise_id, request.json)

@app.route('/exercise/<int:exercise_id>/primary-muscle/<int:muscle_id>', methods=['DELETE'])
def delete_primary_muscle(exercise_id, muscle_id):
    return ExercisePrimaryMusclesHandler().deleteExercisePrimaryMuscle(exercise_id, muscle_id)

@app.route('/exercise/<int:exercise_id>/secondary-muscle', methods=['POST'])
def add_secondary_muscle(exercise_id):
    return ExerciseSecondaryMusclesHandler().insertExerciseSecondaryMuscle(exercise_id, request.json)

@app.route('/exercise/<int:exercise_id>/secondary-muscle/<int:muscle_id>', methods=['DELETE'])
def delete_secondary_muscle(exercise_id, muscle_id):
    return ExerciseSecondaryMusclesHandler().deleteExerciseSecondaryMuscle(exercise_id, muscle_id)

@app.route('/exercise/<int:exercise_id>/sport/<int:sport_id>', methods=['POST'])
def add_sport_to_exercise(exercise_id, sport_id):
    return SportExercisesHandler().insertSportExercise(exercise_id, sport_id)

@app.route('/exercise/<int:exercise_id>/sport/<int:sport_id>', methods=['DELETE'])
def delete_sport_from_exercise(exercise_id, sport_id):
    return SportExercisesHandler().deleteSportExercise(exercise_id, sport_id)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

