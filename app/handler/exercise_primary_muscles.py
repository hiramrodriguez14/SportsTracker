from flask import jsonify
from app.model.dao.exercise_primary_muscles import ExercisePrimaryMusclesDAO

class ExercisePrimaryMusclesHandler:
    def insertExercisePrimaryMuscle(self,eid, json):
        if  'muscle_description' not in json:
            return jsonify({"error": "Missing parameters"}), 400

      
        muscle = json['muscle_description']

        dao = ExercisePrimaryMusclesDAO()

        if not dao.exerciseExists(eid):
            return jsonify({"error": "Exercise ID not found"}), 404

        id = dao.insertExercisePrimaryMuscles(eid, muscle)
        
       
        json["id"]  = id
        return jsonify({"exercise_id": eid,"muscle_id":id,"muscle_description": muscle}), 201

    def deleteExercisePrimaryMuscle(self,exercise_id,muscle_id):

        dao = ExercisePrimaryMusclesDAO()

        if not dao.exerciseExists(exercise_id):
            return jsonify({"error": "Exercise ID not found"}), 404
        if not dao.muscleExists(muscle_id):
            return jsonify({"error": "Exercise ID not found"}), 404

        dao.deleteExercisePrimaryMuscle(exercise_id, muscle_id)
     
        return '', 204
