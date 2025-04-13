from app.config.pgconfig import pgconfig
import psycopg2
import os
from collections import defaultdict

class dao_exercise:
    def __init__(self):
        #self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        url = "dbname=%s password=%s host=%s port=%s user=%s" % (
            pgconfig.DB_NAME,
            pgconfig.DB_PASSWORD,
            pgconfig.DB_HOST,
            pgconfig.DB_PORT,
            pgconfig.DB_USER
        )


        self.conn = psycopg2.connect(url)

    def insert_exercise(self, name, category, equipment, mechanic, force, level, alter_id):
        """Insert a new exercise while preventing duplicates."""
        cursor = self.conn.cursor()

        # Check if exercise already exists
        query = "SELECT id FROM exercises WHERE name = %s"
        cursor.execute(query, (name,))
        if cursor.fetchone():
            cursor.close()
            return {"error": "Exercise already exists", "status": 409}

        # Insert new exercise
        query = """INSERT INTO exercises (name, category, equipment, mechanic, force, level, alter_id) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s) 
                   RETURNING id"""
        cursor.execute(query, (name, category, equipment, mechanic, force, level, alter_id))
        exercise_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return {"id": exercise_id, "status": 201}



    def get_all_exercises(self):
        """Retrieve all exercises."""
        cursor = self.conn.cursor()
        query = "SELECT id, name, category, equipment, mechanic, force, level, alter_id FROM exercises"
        cursor.execute(query)
        exercises = cursor.fetchall()
        cursor.close()
        return exercises



    

    def get_exercise_by_id(self, exercise_id):
        """Retrieve exercise details, including instructions, images, and muscles."""
        cursor = self.conn.cursor()

        # Fetch base exercise data
        query = "SELECT id, name, category, equipment, mechanic, force, level, alter_id FROM exercises WHERE id = %s"
        cursor.execute(query, (exercise_id,))
        exercise = cursor.fetchone()

        if not exercise:
            return None  # Exercise not found

        # Fetch instructions
        query = """SELECT id, instruction_number, instruction 
                   FROM exercise_instructions WHERE exercise_id = %s ORDER BY instruction_number"""
        cursor.execute(query, (exercise_id,))
        instructions = cursor.fetchall()

        # Fetch images
        query = "SELECT id, image_path FROM exercise_images WHERE exercise_id = %s"
        cursor.execute(query, (exercise_id,))
        images = cursor.fetchall()

        # Fetch primary muscles
        query = """SELECT id, muscle 
                    FROM exercise_primary_muscles
                    WHERE exercise_id = %s;"""
        cursor.execute(query, (exercise_id,))
        primary_muscles = cursor.fetchall()

        # Fetch secondary muscles
        query = """SELECT id, muscle 
                    FROM exercise_secondary_muscles 
                    WHERE exercise_id = %s;"""
        cursor.execute(query, (exercise_id,))
        secondary_muscles = cursor.fetchall()

        cursor.close()

        return {
            "id": exercise[0],
            "name": exercise[1],
            "category": exercise[2],
            "equipment": exercise[3],
            "mechanic": exercise[4],
            "force": exercise[5],
            "level": exercise[6],
            "alter_id": exercise[7],
            "instructions": [{"instruction_id": ins[0], "instruction_number": ins[1], "description": ins[2]} for ins in instructions],
            "images": [{"image_id": img[0], "path": img[1]} for img in images],
            "primary_muscles": [{"muscle_id": pm[0], "name": pm[1]} for pm in primary_muscles],
            "secondary_muscles": [{"muscle_id": sm[0], "name": sm[1]} for sm in secondary_muscles],
        }




    def update_exercise(self, exercise_id, name, category, equipment, mechanic, force, level, alter_id):
        """Update an exercise, ensuring it exists."""
        cursor = self.conn.cursor()
        query = "SELECT id FROM exercises WHERE id = %s"
        cursor.execute(query, (exercise_id,))
        if not cursor.fetchone():
            cursor.close()
            return {"error": "Exercise not found", "status": 404}

        query = """UPDATE exercises SET name = %s, category = %s, equipment = %s, 
                   mechanic = %s, force = %s, level = %s, alter_id = %s WHERE id = %s"""
        cursor.execute(query, (name, category, equipment, mechanic, force, level, alter_id, exercise_id))
        self.conn.commit()
        cursor.close()
        return {"status": 200}





    def delete_exercise(self, exercise_id):
        """Delete an exercise while handling foreign key constraints."""
        cursor = self.conn.cursor()
        try:
            query = "DELETE FROM exercises WHERE id = %s"
            cursor.execute(query, (exercise_id,))
            if cursor.rowcount == 0:
                cursor.close()
                return {"error": "Exercise not found", "status": 404}
            
            self.conn.commit()
            cursor.close()
            return {"status": 204}
        except psycopg2.IntegrityError:
            self.conn.rollback()
            cursor.close()
            return {"error": "Cannot delete exercise; it is referenced elsewhere", "status": 409}



    # def get_most_performed_exercises(self):
    #     """Retrieve the top 5 most performed exercises based on primary and secondary muscle occurrences."""
    #     cursor = self.conn.cursor()
    #     query = """
    #         SELECT e.id, e.name, COUNT(*) as times_performed
    #         FROM exercises e
    #         LEFT JOIN (
    #             SELECT exercise_id FROM exercise_primary_muscles
    #             UNION ALL
    #             SELECT exercise_id FROM exercise_secondary_muscles
    #         ) AS all_muscles ON e.id = all_muscles.exercise_id
    #         GROUP BY e.id
    #         ORDER BY times_performed DESC
    #         LIMIT 5;
    #     """
    #     cursor.execute(query)
    #     exercises = cursor.fetchall()
    #     cursor.close()
    #     return [{"id": ex[0], "name": ex[1], "times_performed": ex[2]} for ex in exercises]


    def get_most_performed_exercises(self):
        """Retrieve top 5 most performed exercises based on muscle associations."""
        cursor = self.conn.cursor()
        query = """
            SELECT e.id, e.name, COUNT(*) AS sports_related
            FROM exercises e
            LEFT JOIN (
                SELECT exercise_id FROM exercise_primary_muscles
                UNION ALL
                SELECT exercise_id FROM exercise_secondary_muscles
            ) AS all_muscles ON e.id = all_muscles.exercise_id
            GROUP BY e.id
            ORDER BY sports_related DESC
            LIMIT 5;
        """
        cursor.execute(query)
        exercises = cursor.fetchall()
        cursor.close()
        return [
            {"exercise_id": ex[0], "name": ex[1], "sports_related": ex[2]}
            for ex in exercises
        ]



    # def get_exercises_by_muscle(self, muscle):
    #     """Retrieve exercises that target a specific muscle."""
    #     cursor = self.conn.cursor()
    #     query = """
    #         SELECT DISTINCT e.id, e.name
    #         FROM exercises e
    #         LEFT JOIN exercise_primary_muscles epm ON e.id = epm.exercise_id
    #         LEFT JOIN exercise_secondary_muscles esm ON e.id = esm.exercise_id
    #         WHERE epm.muscle = %s OR esm.muscle = %s;
    #     """
    #     cursor.execute(query, (muscle, muscle))
    #     exercises = cursor.fetchall()
    #     cursor.close()
    #     return [{"id": ex[0], "name": ex[1]} for ex in exercises]


 
    def get_exercises_by_muscle(self, muscle):
        """Retrieve exercises that target a specific muscle group."""
        cursor = self.conn.cursor()
        query = """
            SELECT DISTINCT e.id, e.name
            FROM exercises e
            LEFT JOIN exercise_primary_muscles epm ON e.id = epm.exercise_id
            LEFT JOIN exercise_secondary_muscles esm ON e.id = esm.exercise_id
            WHERE LOWER(epm.muscle) = LOWER(%s) OR LOWER(esm.muscle) = LOWER(%s);
        """
        cursor.execute(query, (muscle, muscle))
        exercises = cursor.fetchall()
        cursor.close()
        return [{"exercise_id": ex[0], "name": ex[1]} for ex in exercises]




    # def get_most_complex_exercises(self):
    #     """Retrieve exercises that target the highest number of different muscle groups."""
    #     cursor = self.conn.cursor()
    #     query = """
    #         SELECT e.id, e.name, COUNT(DISTINCT m.muscle) AS muscle_group_count
    #         FROM exercises e
    #         LEFT JOIN (
    #         SELECT exercise_id, muscle FROM exercise_primary_muscles
    #         UNION
    #         SELECT exercise_id, muscle FROM exercise_secondary_muscles
    #         ) m ON e.id = m.exercise_id
    #         GROUP BY e.id
    #         ORDER BY muscle_group_count DESC;
    #     """
    #     cursor.execute(query)
    #     exercises = cursor.fetchall()
    #     cursor.close()
    #     return [{"id": ex[0], "name": ex[1], "muscle_group_count": ex[2]} for ex in exercises]



    def get_most_complex_exercises(self):
        """Retrieve exercises that engage the most different muscle groups."""
        cursor = self.conn.cursor()

        # Find the maximum number of unique muscles targeted by any exercise
        max_query = """
            SELECT MAX(muscle_count) FROM (
                SELECT e.id, COUNT(DISTINCT m.muscle) AS muscle_count
                FROM exercises e
                LEFT JOIN (
                    SELECT exercise_id, muscle FROM exercise_primary_muscles
                    UNION
                    SELECT exercise_id, muscle FROM exercise_secondary_muscles
                ) m ON e.id = m.exercise_id
                GROUP BY e.id
            ) AS counts;
        """
        cursor.execute(max_query)
        max_count = cursor.fetchone()[0]

        if max_count is None:
            cursor.close()
            return []

        # Get all exercises with that maximum number of muscles
        query = """
            SELECT e.id, e.name, m.muscle
            FROM exercises e
            LEFT JOIN (
                SELECT exercise_id, muscle FROM exercise_primary_muscles
                UNION
                SELECT exercise_id, muscle FROM exercise_secondary_muscles
            ) m ON e.id = m.exercise_id
            WHERE e.id IN (
                SELECT id FROM (
                    SELECT e.id, COUNT(DISTINCT m.muscle) AS muscle_count
                    FROM exercises e
                    LEFT JOIN (
                        SELECT exercise_id, muscle FROM exercise_primary_muscles
                        UNION
                        SELECT exercise_id, muscle FROM exercise_secondary_muscles
                    ) m ON e.id = m.exercise_id
                    GROUP BY e.id
                ) AS counts
                WHERE muscle_count = %s
            )
            ORDER BY e.id;
        """
        cursor.execute(query, (max_count,))
        rows = cursor.fetchall()
        cursor.close()

        # Group results by exercise_id
        grouped = defaultdict(lambda: {"exercise_id": None, "name": "", "muscle_groups": []})

        for ex_id, name, muscle in rows:
            grouped[ex_id]["exercise_id"] = ex_id
            grouped[ex_id]["name"] = name
            grouped[ex_id]["muscle_groups"].append(muscle)

        return list(grouped.values())



    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
