from bug_handling.choose_db import get_db_config
import psycopg2

class SportDAO:
    def __init__(self):
        self.conn = psycopg2.connect(get_db_config().connection_url)

    def getAllSports(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM sports;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getSportByIdWithExercises(self, sport_id):
        cursor = self.conn.cursor()
        query = """
            SELECT s.id, s.name, s.gender, s.venue, e.id, e.name
            FROM sports s
            LEFT JOIN exercise_sports es ON s.id = es.sports_id
            LEFT JOIN exercise e ON es.exercise_id = e.id
            WHERE s.id = %s;
        """
        cursor.execute(query, (sport_id,))
        rows = cursor.fetchall()
        cursor.close()

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

    def insertSport(self, name, gender, venue):
        cursor = self.conn.cursor()
        query = "INSERT INTO sports(name, gender, venue) VALUES (%s, %s, %s) RETURNING id;"
        cursor.execute(query, (name, gender, venue))
        sport_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return sport_id

    def updateSport(self, sport_id, name, gender, venue):
        cursor = self.conn.cursor()
        query = "UPDATE sports SET name = %s, gender = %s, venue = %s WHERE id = %s;"
        cursor.execute(query, (name, gender, venue, sport_id))
        self.conn.commit()
        cursor.close()
        return True

    def deleteSport(self, sport_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM sports WHERE id = %s;"
        cursor.execute(query, (sport_id,))
        self.conn.commit()
        cursor.close()
        return True