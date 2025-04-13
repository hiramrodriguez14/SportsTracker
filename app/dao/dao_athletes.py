from bug_handling.choose_db import get_db_config
import psycopg2

class AthleteDAO:
    def __init__(self):
        self.conn = psycopg2.connect(get_db_config().connection_url)

    def get_all_athletes(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM athletes")
        results = cursor.fetchall()
        cursor.close()
        return results

    def get_athlete_by_id(self, athlete_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM athletes WHERE id = %s", (athlete_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def create_athlete(self, athlete_id, name, age, gender, height, weight):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO athletes (id, name, age, gender, height, weight)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (athlete_id, name, age, gender, height, weight))
        self.conn.commit()
        cursor.close()
        return athlete_id

    def update_athlete(self, athlete_id, name, age, gender, height, weight):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE athletes SET name=%s, age=%s, height=%s, weight=%s, gender=%s
            WHERE id=%s
        """, (name, age, height, weight, gender, athlete_id))
        self.conn.commit()
        cursor.close()
        return True

    def delete_athlete(self, athlete_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM athletes WHERE id = %s", (athlete_id,))
        self.conn.commit()
        cursor.close()
        return True
