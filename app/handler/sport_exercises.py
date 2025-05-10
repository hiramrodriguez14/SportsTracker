from flask import jsonify
from app.model.dao.sport_exercises import SportExercisesDAO

class SportExercisesHandler:
    def insertSportExercise(self, eid, sid):

        dao = SportExercisesDAO()


        if not dao.exerciseExist(eid):
            return jsonify({"error": "Exercise ID not found"}), 404

        if not dao.sportExist(sid):
            return jsonify({"error": "Sport ID not found"}), 404
   
        dao.insertSportExercise(eid, sid)
        return jsonify({"exercise_id": eid, "sport_id":sid}), 201
     
        
    def deleteSportExercise(self, eid, sid):

        dao = SportExercisesDAO()


        if not dao.exerciseExist(eid):
            return jsonify({"error": "Exercise ID not found"}), 404

        if not dao.sportExist(sid):
            return jsonify({"error": "Sport ID not found"}), 404
   
        dao.deleteSportExercise(eid, sid)
        return '', 204