from bug_handling.choose_db import get_db_config
import psycopg2

class TeamsDAO:
    def __init__(self):
        self.conn = psycopg2.connect(get_db_config().connection_url)

    def sportExists(self, sid):
        cursor = self.conn.cursor()
        query = "SELECT 1 FROM sports WHERE id = %s"
        cursor.execute(query, (sid,))
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def teamExists(self, id):
        cursor = self.conn.cursor()
        query = "SELECT 1 FROM teams WHERE id = %s"
        cursor.execute(query, (id,))
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def teamReferences(self, id):
        cursor = self.conn.cursor()
        query = "SELECT 1 FROM practices WHERE fk_team = %s"
        cursor.execute(query, (id,))
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def insertTeam(self, sid, name):    
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO teams (name, sport) VALUES (%s, %s) RETURNING id",
            (name, sid)
        )
        id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return id

    def getAllTeams(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM teams")
        result = []
        for row in cursor:
            result.append({
                "id": row[0],
                "name": row[1],
                "sport": row[2]
            })
        cursor.close()
        return result

    def getTeamByID(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM teams WHERE id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return {
                "id": result[0],
                "name": result[1],
                "sport_id": result[2]
            }
        else:
            return None

    def updateTeam(self, id, name, sport):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE teams SET name = %s, sport = %s WHERE id = %s",
            (name, sport, id)
        )
        self.conn.commit()
        cursor.close()
        return True

    def deleteTeam(self, id):
        cursor = self.conn.cursor()
        query = "DELETE FROM teams WHERE id = %s"
        cursor.execute(query, (id,))
        self.conn.commit()
        cursor.close()
        return True
