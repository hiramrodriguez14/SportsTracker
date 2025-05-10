import psycopg2
from bug_handling.choose_db import get_db_config

class AthleteDAO:

    def get_all_athletes(self):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM athletes")
                result = cursor.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] get_all_athletes: {e}")
            conn.rollback()
            conn.close()
            return []

    def get_athlete_by_id(self, athlete_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM athletes WHERE id = %s", (athlete_id,))
                result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] get_athlete_by_id: {e}")
            conn.rollback()
            conn.close()
            return None

    def create_athlete(self, name, age, gender, height, weight):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO athletes (name, age, gender, height, weight)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (name, age, gender, height, weight))
                athlete_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return athlete_id
        except Exception as e:
            print(f"[ERROR] create_athlete: {e}")
            conn.rollback()
            conn.close()
            return None

    def update_athlete(self, athlete_id, name, age, gender, height, weight):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE athletes
                    SET name=%s, age=%s, height=%s, weight=%s, gender=%s
                    WHERE id=%s
                """, (name, age, height, weight, gender, athlete_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] update_athlete: {e}")
            conn.rollback()
            conn.close()
            return False

    def delete_athlete(self, athlete_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM athletes WHERE id = %s", (athlete_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] delete_athlete: {e}")
            conn.rollback()
            conn.close()
            return False
