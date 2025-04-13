from flask import jsonify
from app.dao.sport_exercises import SportExercisesDAO

class SportExercisesHandler:
    def insertSportExercise(self, sid, eid):

        dao = SportExercisesDAO()


        if not dao.exerciseExist(eid):
            return jsonify({"error": "Exercise ID not found"}), 404

        if not dao.sportExist(sid):
            return jsonify({"error": "Sport ID not found"}), 404
   
        dao.insertSportExercise(sid, eid)
        return jsonify({"exercise_id": eid, "sport_id":sid}), 201
     
        
    def deleteSportExercise(self, sid, eid):

        dao = SportExercisesDAO()


        if not dao.exerciseExist(eid):
            return jsonify({"error": "Exercise ID not found"}), 404

        if not dao.sportExist(sid):
            return jsonify({"error": "Sport ID not found"}), 404
   
        dao.deleteSportExercise(sid, eid)
        return '', 204
     
