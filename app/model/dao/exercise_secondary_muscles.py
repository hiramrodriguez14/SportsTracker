import psycopg2
from bug_handling.choose_db import get_db_config

class ExerciseSecondaryMusclesDAO:

    def exerciseExists(self, eid):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM exercises WHERE id = %s", (eid,))
                result = cursor.fetchone() is not None
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] exerciseExists: {e}")
            conn.rollback()
            conn.close()
            return False

    def muscleExists(self, muscle_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM exercise_secondary_muscles WHERE id = %s", (muscle_id,))
                result = cursor.fetchone() is not None
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] muscleExists: {e}")
            conn.rollback()
            conn.close()
            return False

    def insertExerciseSecondaryMuscle(self, eid, muscle):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO exercise_secondary_muscles (exercise_id, muscle) VALUES (%s, %s) RETURNING id",
                    (eid, muscle)
                )
                inserted_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return inserted_id
        except Exception as e:
            print(f"[ERROR] insertExerciseSecondaryMuscle: {e}")
            conn.rollback()
            conn.close()
            return None

    def deleteExerciseSecondaryMuscle(self, eid, muscle_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM exercise_secondary_muscles WHERE exercise_id = %s AND id = %s",
                    (eid, muscle_id)
                )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] deleteExerciseSecondaryMuscle: {e}")
            conn.rollback()
            conn.close()
            return False
