import psycopg2
from bug_handling.choose_db import get_db_config

class AnalyticsDAO:
    def __init__(self):
        self.conn = psycopg2.connect(get_db_config().connection_url)

    def getTopTeams(self):
        cursor = self.conn.cursor()
        query = """
            SELECT t.id, t.name, s.name, COUNT(*) as wins
            FROM championships c
            JOIN teams t ON c.winner_team = t.id
            JOIN sports s ON t.sport = s.id
            GROUP BY t.id, t.name, s.name
            ORDER BY wins DESC
            LIMIT 3;
        """

        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getSportsDistribution(self):
        cursor = self.conn.cursor()
        query = """
            SELECT sports.name as sport, COUNT(teams.sport) as team_count
            FROM sports
            JOIN teams ON (teams.sport = sports.id)
            GROUP BY sports.name, teams.sport
            ORDER BY sport ASC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getMostChampionshipWins(self):
        cursor = self.conn.cursor()
        query = """
            SELECT t.id, t.name, COUNT(*) as total_wins
            FROM championships c
            JOIN teams t ON c.winner_team = t.id
            GROUP BY t.id, t.name
            ORDER BY total_wins DESC
            LIMIT 5;
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def getSportPopularity(self):
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT s.name, COUNT(a.id) as athlete_count
                FROM athletes a
                JOIN practices p ON a.id = p.fk_athlete
                JOIN teams t ON p.fk_team = t.id
                JOIN sports s ON t.sport = s.id
                GROUP BY s.name
                ORDER BY athlete_count DESC
                LIMIT 5;
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            self.conn.rollback()
            raise e

