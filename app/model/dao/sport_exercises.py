import psycopg2
from bug_handling.choose_db import get_db_config

class SportExercisesDAO:

    def exerciseExist(self, eid):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM exercises WHERE id = %s", (eid,))
                result = cursor.fetchone() is not None
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] exerciseExist: {e}")
            conn.rollback()
            conn.close()
            return False

    def sportExist(self, sid):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM sports WHERE id = %s", (sid,))
                result = cursor.fetchone() is not None
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] sportExist: {e}")
            conn.rollback()
            conn.close()
            return False

    def insertSportExercise(self, eid, sid):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO sport_exercises (sport, exercise) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (sid, eid)
                )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] insertSportExercise: {e}")
            conn.rollback()
            conn.close()
            return False

    def deleteSportExercise(self, eid, sid):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM sport_exercises WHERE sport = %s AND exercise = %s",
                    (sid, eid)
                )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] deleteSportExercise: {e}")
            conn.rollback()
            conn.close()
            return False
