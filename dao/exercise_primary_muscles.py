import psycopg2
from app.config.pgconfig import pgconfig

class ExercisePrimaryMusclesDAO:
    def __init__(self):
        url = "dbname= %s password = %s host = %s port = %s user = %s" % (
            pgconfig.DB_NAME,
            pgconfig.DB_PASSWORD,
            pgconfig.DB_HOST,
            pgconfig.DB_PORT,
            pgconfig.DB_USER
        )
        self.conn = psycopg2.connect(url)

    def exerciseExists(self, eid):
        cursor = self.conn.cursor()
        query = "SELECT 1 FROM exercises WHERE id = %s"
        cursor.execute(query, (eid,))
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists
    
    def muscleExists(self, muscle_id):
        cursor = self.conn.cursor()
        query = "SELECT 1 FROM exercise_primary_muscles WHERE id = %s"
        cursor.execute(query, (muscle_id,))
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def insertExercisePrimaryMuscles(self, eid, muscle):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO exercise_primary_muscles (exercise_id, muscle) VALUES (%s, %s) returning id",
            (eid, muscle)
        )
        id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return id

    def deleteExercisePrimaryMuscle(self, eid, muscle_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM exercise_primary_muscles WHERE exercise_id = %s AND id = %s",
            (eid, muscle_id)
        )
        self.conn.commit()
        cursor.close()
        return 
