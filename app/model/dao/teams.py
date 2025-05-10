import psycopg2
from bug_handling.choose_db import get_db_config

class TeamsDAO:

    def sportExists(self, sid):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM sports WHERE id = %s", (sid,))
                result = cursor.fetchone() is not None
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] sportExists: {e}")
            conn.rollback()
            conn.close()
            return False

    def teamExists(self, id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM teams WHERE id = %s", (id,))
                result = cursor.fetchone() is not None
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] teamExists: {e}")
            conn.rollback()
            conn.close()
            return False

    def teamReferences(self, id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM practices WHERE fk_team = %s", (id,))
                result = cursor.fetchone() is not None
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] teamReferences: {e}")
            conn.rollback()
            conn.close()
            return False

    def insertTeam(self, sid, name):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO teams (name, sport) VALUES (%s, %s) RETURNING id",
                    (name, sid)
                )
                inserted_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return inserted_id
        except Exception as e:
            print(f"[ERROR] insertTeam: {e}")
            conn.rollback()
            conn.close()
            return None

    def getAllTeams(self):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM teams")
                result = [
                    {"id": row[0], "name": row[1], "sport": row[2]}
                    for row in cursor
                ]
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] getAllTeams: {e}")
            conn.rollback()
            conn.close()
            return []

    def getTeamByID(self, id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM teams WHERE id = %s", (id,))
                result = cursor.fetchone()
            conn.close()
            if result:
                return {
                    "id": result[0],
                    "name": result[1],
                    "sport_id": result[2]
                }
            else:
                return None
        except Exception as e:
            print(f"[ERROR] getTeamByID: {e}")
            conn.rollback()
            conn.close()
            return None

    def updateTeam(self, id, name, sport):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE teams SET name = %s, sport = %s WHERE id = %s",
                    (name, sport, id)
                )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] updateTeam: {e}")
            conn.rollback()
            conn.close()
            return False

    def deleteTeam(self, id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM teams WHERE id = %s", (id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] deleteTeam: {e}")
            conn.rollback()
            conn.close()
            return False
