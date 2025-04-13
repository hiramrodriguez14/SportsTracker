from app.dao.dao_exercise import dao_exercise
from flask import jsonify

dao = dao_exercise()

class ExerciseHandler:
    
    def create_exercise(self, data):
        """Create a new exercise."""
        if not all(k in data for k in ("name", "category", "equipment", "mechanic", "force", "level", "alter_id")):
            return jsonify({"error": "Missing required fields"}), 400

        exercise_id = dao.insert_exercise(
            data["name"], data["category"], data["equipment"], 
            data["mechanic"], data["force"], data["level"], data["alter_id"]
        )

        data["id"] = exercise_id
        return jsonify(data), 201





    def get_all_exercises(self):
        """Retrieve all exercises."""
        exercises = dao.get_all_exercises()
        exercise_list = [
            {
                "id": ex[0],
                "name": ex[1],
                "category": ex[2],
                "equipment": ex[3],
                "mechanic": ex[4],
                "force": ex[5],
                "level": ex[6],
                "alter_id": ex[7]
            } for ex in exercises
        ]
        return jsonify(exercise_list), 200





    def get_exercise(self, exercise_id):
        """Retrieve exercise details by ID."""
        exercise = dao.get_exercise_by_id(exercise_id)
        if exercise is None:
            return jsonify({"error": "Exercise not found"}), 404
        return jsonify(exercise), 200




    def update_exercise(self, exercise_id, data):
        """Update an exercise’s details."""
        if not all(k in data for k in ("name", "category", "equipment", "mechanic", "force", "level", "alter_id")):
            return jsonify({"error": "Missing required fields"}), 400

        success = dao.update_exercise(
            exercise_id, data["name"], data["category"], data["equipment"], 
            data["mechanic"], data["force"], data["level"], data["alter_id"]
        )

        if not success:
            return jsonify({"error": "Exercise not found"}), 404

        return jsonify(data), 200





    def delete_exercise(self, exercise_id):
        """Delete an exercise."""
        success = dao.delete_exercise(exercise_id)
        if not success:
            return jsonify({"error": "Exercise not found"}), 404

        return "", 204



    def get_most_performed_exercises(self):
        exercises = dao.get_most_performed_exercises()
        return jsonify(exercises), 200

    def get_exercises_by_muscle(self, muscle):
        exercises = dao.get_exercises_by_muscle(muscle)
        return jsonify(exercises), 200

    def get_most_complex_exercises(self):
        exercises = dao.get_most_complex_exercises()
        return jsonify(exercises), 200
