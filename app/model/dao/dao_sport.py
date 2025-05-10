from bug_handling.choose_db import get_db_config
import psycopg2

class SportDAO:

    def getAllSports(self):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM sports;")
                result = cursor.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] getAllSports: {e}")
            conn.rollback()
            conn.close()
            return []

    def getSportByIdWithExercises(self, sport_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                query = """
                    SELECT s.id, s.name, s.gender, s.venue, e.id, e.name
                    FROM sports s
                    LEFT JOIN sport_exercises es ON s.id = es.sport
                    LEFT JOIN exercises e ON es.exercise = e.id
                    WHERE s.id = %s;
                """
                cursor.execute(query, (sport_id,))
                rows = cursor.fetchall()
            conn.close()

            if not rows:
                return None

            sport_info = rows[0][:4]
            exercises = []
            for row in rows:
                if row[4]:
                    exercises.append({"id": row[4], "name": row[5]})

            return {
                "id": sport_info[0],
                "name": sport_info[1],
                "gender": sport_info[2],
                "venue": sport_info[3],
                "exercises": exercises
            }
        except Exception as e:
            print(f"[ERROR] getSportByIdWithExercises: {e}")
            return None

    def insertSport(self, name, gender, venue):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                query = "INSERT INTO sports(name, gender, venue) VALUES (%s, %s, %s) RETURNING id;"
                cursor.execute(query, (name, gender, venue))
                sport_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return sport_id
        except Exception as e:
            print(f"[ERROR] insertSport: {e}")
            conn.rollback()
            conn.close()
            return None

    def updateSport(self, sport_id, name, gender, venue):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                query = "UPDATE sports SET name = %s, gender = %s, venue = %s WHERE id = %s;"
                cursor.execute(query, (name, gender, venue, sport_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] updateSport: {e}")
            conn.rollback()
            conn.close()
            return False

    def deleteSport(self, sport_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                query = "DELETE FROM sports WHERE id = %s;"
                cursor.execute(query, (sport_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] deleteSport: {e}")
            conn.rollback()
            conn.close()
            return False
