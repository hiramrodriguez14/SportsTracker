from flask import jsonify
from dao.exercise_secondary_muscles import ExerciseSecondaryMusclesDAO

class ExerciseSecondaryMusclesHandler:
    def insertExerciseSecondaryMuscles(self,eid, json):
        if  'muscle_description' not in json:
            return jsonify({"error": "Missing parameters"}), 400

      
        muscle = json['muscle_description']

        dao = ExerciseSecondaryMusclesDAO()

        if not dao.exerciseExists(eid):
            return jsonify({"error": "Exercise ID not found"}), 404

        id = dao.insertExerciseSecondaryMuscles(eid, muscle)
        
       
        json["id"]  = id
        return jsonify({"exercise_id": eid,"muscle_id":id,"message": muscle}), 201

    def deleteExerciseInstruction(self,exercise_id,muscle_id):

        dao = ExerciseSecondaryMusclesDAO()

        if not dao.exerciseExists(exercise_id):
            return jsonify({"error": "Exercise ID not found"}), 404
        if not dao.muscleExists(muscle_id):
            return jsonify({"error": "Exercise ID not found"}), 404

        dao.deleteExerciseInstruction(exercise_id, muscle_id)
     
        return '', 204
