import psycopg2
from bug_handling.choose_db import get_db_config

class ExerciseImageDAO:

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

    def imageExists(self, image_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM exercise_images WHERE id = %s", (image_id,))
                result = cursor.fetchone() is not None
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] imageExists: {e}")
            conn.rollback()
            conn.close()
            return False

    def insertExerciseImage(self, eid, path):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO exercise_images (exercise_id, image_path) VALUES (%s, %s) RETURNING id",
                    (eid, path)
                )
                image_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return image_id
        except Exception as e:
            print(f"[ERROR] insertExerciseImage: {e}")
            conn.rollback()
            conn.close()
            return None

    def deleteExerciseImage(self, eid, image_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM exercise_images WHERE exercise_id = %s AND id = %s",
                    (eid, image_id)
                )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] deleteExerciseImage: {e}")
            conn.rollback()
            conn.close()
            return False
