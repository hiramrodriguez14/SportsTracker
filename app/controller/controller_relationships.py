from flask import Blueprint, request
from app.handler.exercise_instructions import ExerciseInstructionsHandler
from app.handler.exercise_image import ExerciseImageHandler
from app.handler.exercise_primary_muscles import ExercisePrimaryMusclesHandler
from app.handler.exercise_secondary_muscles import ExerciseSecondaryMusclesHandler
from app.handler.sport_exercises import SportExercisesHandler

relationships_routes = Blueprint("relationships_routes", __name__)

@relationships_routes.route("/exercise/<int:exercise_id>/instruction", methods=["POST"])
def add_instruction(exercise_id):
    return ExerciseInstructionsHandler().insertExerciseInstruction(exercise_id, request.json)

@relationships_routes.route("/exercise/<int:exercise_id>/instruction/<int:instruction_id>", methods=["DELETE"])
def delete_instruction(exercise_id, instruction_id):
    return ExerciseInstructionsHandler().deleteExerciseInstruction(exercise_id, instruction_id)

@relationships_routes.route("/exercise/<int:exercise_id>/image", methods=["POST"])
def add_image(exercise_id):
    return ExerciseImageHandler().insertExerciseImage(exercise_id, request.json)

@relationships_routes.route("/exercise/<int:exercise_id>/image/<int:image_id>", methods=["DELETE"])
def delete_image(exercise_id, image_id):
    return ExerciseImageHandler().deleteExerciseImage(exercise_id, image_id)

@relationships_routes.route("/exercise/<int:exercise_id>/primary-muscle", methods=["POST"])
def add_primary(exercise_id):
    return ExercisePrimaryMusclesHandler().insertExercisePrimaryMuscle(exercise_id, request.json)

@relationships_routes.route("/exercise/<int:exercise_id>/primary-muscle/<int:muscle_id>", methods=["DELETE"])
def delete_primary(exercise_id, muscle_id):
    return ExercisePrimaryMusclesHandler().deleteExercisePrimaryMuscle(exercise_id, muscle_id)

@relationships_routes.route("/exercise/<int:exercise_id>/secondary-muscle", methods=["POST"])
def add_secondary(exercise_id):
    return ExerciseSecondaryMusclesHandler().insertExerciseSecondaryMuscle(exercise_id, request.json)

@relationships_routes.route("/exercise/<int:exercise_id>/secondary-muscle/<int:muscle_id>", methods=["DELETE"])
def delete_secondary(exercise_id, muscle_id):
    return ExerciseSecondaryMusclesHandler().deleteExerciseSecondaryMuscle(exercise_id, muscle_id)

@relationships_routes.route("/exercise/<int:exercise_id>/sport/<int:sport_id>", methods=["POST"])
def add_sport(exercise_id, sport_id):
    return SportExercisesHandler().insertSportExercise(exercise_id, sport_id)

@relationships_routes.route("/exercise/<int:exercise_id>/sport/<int:sport_id>", methods=["DELETE"])
def delete_sport(exercise_id, sport_id):
    return SportExercisesHandler().deleteSportExercise(exercise_id, sport_id)
