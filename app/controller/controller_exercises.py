from flask import Blueprint, request, jsonify
from app.handler.exercise import ExerciseHandler

exercise_routes = Blueprint("exercise_routes", __name__)
handler = ExerciseHandler()

@exercise_routes.route("/exercise", methods=["GET"])
def get_all_exercises():
    return handler.get_all_exercises()

@exercise_routes.route("/exercise/<int:exercise_id>", methods=["GET", "PUT", "DELETE"])
def exercise_crud(exercise_id):
    if request.method == "GET":
        return handler.get_exercise(exercise_id)
    elif request.method == "PUT":
        return handler.update_exercise(exercise_id, request.json)
    elif request.method == "DELETE":
        return handler.delete_exercise(exercise_id)

@exercise_routes.route("/exercise", methods=["POST"])
def create_exercise():
    return handler.create_exercise(request.json)

@exercise_routes.route("/exercises/most-performed", methods=["GET"])
def get_most_performed_exercises():
    return handler.get_most_performed_exercises()

@exercise_routes.route("/exercises/muscle-group", methods=["GET"])
def get_exercises_by_muscle():
    muscle = request.args.get("muscle")
    if not muscle:
        return jsonify({"error": "Missing 'muscle' parameter"}), 400
    return handler.get_exercises_by_muscle(muscle)

@exercise_routes.route("/exercises/most-complex", methods=["GET"])
def get_most_complex_exercises():
    return handler.get_most_complex_exercises()
