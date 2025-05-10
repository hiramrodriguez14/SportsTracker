from bug_handling.choose_db import get_db_config
import psycopg2

class ChampionshipDAO:

    def getAllChampionships(self):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM championships;")
                result = cursor.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] getAllChampionships: {e}")
            conn.rollback()
            conn.close()
            return None

    def getChampionshipByIdWithWinner(self, champ_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                query = """
                    SELECT c.id, c.name, c.winner_year, t.id, t.name
                    FROM championships c
                    LEFT JOIN teams t ON c.winner_team = t.id
                    WHERE c.id = %s;
                """
                cursor.execute(query, (champ_id,))
                row = cursor.fetchone()
            conn.close()

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
        except Exception as e:
            print(f"[ERROR] getChampionshipByIdWithWinner: {e}")
            return None

    def insertChampionship(self, name, year, winner_team_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                query = """
                    INSERT INTO championships(name, winner_year, winner_team)
                    VALUES (%s, %s, %s)
                    RETURNING id;
                """
                cursor.execute(query, (name, year, winner_team_id))
                champ_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return champ_id
        except Exception as e:
            print(f"[ERROR] insertChampionship: {e}")
            conn.rollback()
            conn.close()
            return None

    def updateChampionship(self, champ_id, name, year, winner_team_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                query = """
                    UPDATE championships
                    SET name = %s, winner_year = %s, winner_team = %s
                    WHERE id = %s;
                """
                cursor.execute(query, (name, year, winner_team_id, champ_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] updateChampionship: {e}")
            conn.rollback()
            conn.close()
            return False

    def deleteChampionship(self, champ_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                query = "DELETE FROM championships WHERE id = %s;"
                cursor.execute(query, (champ_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] deleteChampionship: {e}")
            conn.rollback()
            conn.close()
            return False
