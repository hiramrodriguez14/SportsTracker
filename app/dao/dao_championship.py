from bug_handling.choose_db import get_db_config
import psycopg2

class ChampionshipDAO:
    def __init__(self):
        self.conn = psycopg2.connect(get_db_config().connection_url)
        
    def getAllChampionships(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM championships;"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getChampionshipByIdWithWinner(self, champ_id):
        cursor = self.conn.cursor()
        query = """
            SELECT c.id, c.name, c.winner_year, t.id, t.name
            FROM championships c
            LEFT JOIN teams t ON c.winner_team = t.id
            WHERE c.id = %s;
        """
        cursor.execute(query, (champ_id,))
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "year": row[2],
            "winner_team": {
                "team_id": row[3],
                "name": row[4]
            } if row[3] else None
        }

    def insertChampionship(self, name, year, winner_team_id):
        cursor = self.conn.cursor()
        query = "INSERT INTO championships(name, winner_year, winner_team) VALUES (%s, %s, %s) RETURNING id;"
        cursor.execute(query, (name, year, winner_team_id))
        champ_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return champ_id

    def updateChampionship(self, champ_id, name, year, winner_team_id):
        cursor = self.conn.cursor()
        query = "UPDATE championships SET name = %s, winner_year = %s, winner_team = %s WHERE id = %s;"
        cursor.execute(query, (name, year, winner_team_id, champ_id))
        self.conn.commit()
        cursor.close()
        return True

    def deleteChampionship(self, champ_id):
        cursor = self.conn.cursor()
        query = "DELETE FROM championships WHERE id = %s;"
        cursor.execute(query, (champ_id,))
        self.conn.commit()
        cursor.close()
        return True