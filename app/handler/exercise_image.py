from flask import jsonify
from app.model.dao.exercise_image import ExerciseImageDAO

class ExerciseImageHandler:
    def insertExerciseImage(self, exercise_id, json):
        if "path" not in json:
            return jsonify({"error": "Missing parameters"}), 400
        
        path = json["path"]
        
        dao = ExerciseImageDAO()
        if not dao.exerciseExists(exercise_id):
            return jsonify({"error": "Exercise ID not found"}), 404
        id = dao.insertExerciseImage(exercise_id, path)
        
        json["id"] = id
        return jsonify({"image_id": id, "exercise_id": exercise_id, "path": path}), 201
    
    def deleteExerciseImage(self, exercise_id, image_id):
        
        dao=ExerciseImageDAO()
        
        if not dao.exerciseExists(exercise_id):
            return jsonify({"error": "Exercise ID not found"}), 404
        if not dao.imageExists(image_id):
            return jsonify({"error": "Image ID not found"}), 404
        
        dao.deleteExerciseImage(exercise_id, image_id)
        return '', 204
