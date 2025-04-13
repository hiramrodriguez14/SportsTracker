from flask import jsonify
from dao.exercise_instructions import ExerciseInstructionsDAO

class ExerciseInstructionsHandler:
    def insertExerciseInstruction(self, exercise_id, json):
        if 'instruction_number' not in json or 'description' not in json:
            return jsonify({"error": "Missing parameters"}), 400

        num = json['instruction_number']
        instr = json['description']

        dao = ExerciseInstructionsDAO()

        if not dao.exerciseExists(exercise_id): #Verificar
            return jsonify({"error": "Exercise ID not found"}), 404

        inserted_id = dao.insertExerciseInstruction(exercise_id, num, instr)

        return jsonify({
            "instruction_id": inserted_id,
            "exercise_id": exercise_id,
            "instruction_number": num,
            "description": instr
        }), 201 

    def deleteExerciseInstruction(self, exercise_id, instruction_id):
        dao = ExerciseInstructionsDAO()

        if not dao.exerciseExists(exercise_id):
            return jsonify({"error": "Exercise ID not found"}), 404
        
        if not dao.instructionExists(instruction_id):
            return jsonify({"error": "Instruction ID not found"}), 404

        dao.deleteExerciseInstruction(exercise_id, instruction_id)

        return '', 204 

