import psycopg2
from app.config.pgconfig import pgconfig

class SportExercisesDAO():
    def __init__(self):
        url = "dbname= %s password = %s host = %s port = %s user = %s" % (
            pgconfig.DB_NAME,
            pgconfig.DB_PASSWORD,
            pgconfig.DB_HOST,
            pgconfig.DB_PORT,
            pgconfig.DB_USER
        )
        self.conn = psycopg2.connect(url)
        
    def exerciseExist(self, eid):
            cursor = self.conn.cursor()
            query = "SELECT 1 FROM exercises WHERE id = %s", (eid,)
            cursor.execute(query)
            exists = cursor.fetchone() is not None
            cursor.close()
            return exists
        
    def sportExist(self, sid):
            cursor = self.conn.cursor()
            query = "SELECT 1 FROM sport WHERE id = %s", (sid,)
            cursor.execute(query)
            exists = cursor.fetchone() is not None
            cursor.close()
            return exists
        
    def insertSportExercise(self, sid, eid):    
            cursor = self.conn.cursor()
            cursor.execute(
                    "INSERT INTO sport_exercises (sport, exercise) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                    (sid, eid)
                )
            self.conn.commit()
            cursor.close()
            return 
    
    def deleteSportExercise(self, sid, eid):
            cursor = self.conn.cursor()
            cursor.execute(
                "DELETE FROM sport_exercises WHERE sport = %s AND exercise = %s",
                (sid, eid)
            )
            self.conn.commit()
            cursor.close()
            return 
        
