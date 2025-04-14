import psycopg2
from bug_handling.choose_db import get_db_config

class SportExercisesDAO():
    def __init__(self):
        self.conn = psycopg2.connect(get_db_config().connection_url)
        
    def exerciseExist(self, eid):
        cursor = self.conn.cursor()
        query = "SELECT 1 FROM exercises WHERE id = %s"
        cursor.execute(query, (eid,))  # Corrected here
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists
        
    def sportExist(self, sid):
        cursor = self.conn.cursor()
        query = "SELECT 1 FROM sports WHERE id = %s"
        cursor.execute(query, (sid,))  # Corrected here
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists
        
    def insertSportExercise(self, eid, sid):    
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO sport_exercises (sport, exercise) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (sid, eid)
        )
        self.conn.commit()
        cursor.close()
        return 
    
    def deleteSportExercise(self, eid, sid):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM sport_exercises WHERE sport = %s AND exercise = %s",
            (sid, eid)
        )
        self.conn.commit()
        cursor.close()
        return 
