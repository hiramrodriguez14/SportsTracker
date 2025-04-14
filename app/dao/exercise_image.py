import psycopg2
from bug_handling.choose_db import get_db_config

class ExerciseImageDAO():
    def __init__(self):
        self.conn = psycopg2.connect(get_db_config().connection_url)
        
    def exerciseExists(self, eid):
        cursor = self.conn.cursor()
        query = "SELECT 1 FROM exercises WHERE id = %s"
        cursor.execute(query, (eid,)) 
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists
        
    def imageExists(self, image_id):
        cursor = self.conn.cursor()
        query = "SELECT 1 FROM exercise_images WHERE id = %s"
        cursor.execute(query, (image_id,)) 
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists   
         
    def insertExerciseImage(self, eid, path):  
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO exercise_images (exercise_id, image_path) VALUES (%s, %s) returning id", 
            (eid, path)
        )
        id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return id
    
    def deleteExerciseImage(self, eid, image_id):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM exercise_images WHERE exercise_id = %s AND id = %s", 
            (eid, image_id)
        )
        self.conn.commit()
        cursor.close()
        return True
