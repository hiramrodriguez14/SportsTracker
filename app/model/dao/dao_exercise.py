import psycopg2
from collections import defaultdict
from bug_handling.choose_db import get_db_config

class dao_exercise:

    def insert_exercise(self, name, category, equipment, mechanic, force, level, alter_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO exercises (name, category, equipment, mechanic, force, level, alter_id)
                       VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                    (name, category, equipment, mechanic, force, level, alter_id)
                )
                exercise_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return exercise_id
        except Exception as e:
            print(f"[ERROR] insert_exercise: {e}")
            conn.rollback()
            conn.close()
            return None

    def get_all_exercises(self):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name, category, equipment, mechanic, force, level, alter_id FROM exercises")
                result = cursor.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] get_all_exercises: {e}")
            return []

    def get_exercise_by_id(self, exercise_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name, category, equipment, mechanic, force, level, alter_id FROM exercises WHERE id = %s", (exercise_id,))
                exercise = cursor.fetchone()
                if not exercise:
                    conn.close()
                    return None

                cursor.execute("SELECT id, instruction_number, instruction FROM exercise_instructions WHERE exercise_id = %s ORDER BY instruction_number", (exercise_id,))
                instructions = cursor.fetchall()
                cursor.execute("SELECT id, image_path FROM exercise_images WHERE exercise_id = %s", (exercise_id,))
                images = cursor.fetchall()
                cursor.execute("SELECT id, muscle FROM exercise_primary_muscles WHERE exercise_id = %s", (exercise_id,))
                primary_muscles = cursor.fetchall()
                cursor.execute("SELECT id, muscle FROM exercise_secondary_muscles WHERE exercise_id = %s", (exercise_id,))
                secondary_muscles = cursor.fetchall()
            conn.close()

            return {
                "id": exercise[0],
                "name": exercise[1],
                "category": exercise[2],
                "equipment": exercise[3],
                "mechanic": exercise[4],
                "force": exercise[5],
                "level": exercise[6],
                "alter_id": exercise[7],
                "instructions": [{"instruction_id": i[0], "instruction_number": i[1], "description": i[2]} for i in instructions],
                "images": [{"image_id": img[0], "path": img[1]} for img in images],
                "primary_muscles": [{"muscle_id": pm[0], "name": pm[1]} for pm in primary_muscles],
                "secondary_muscles": [{"muscle_id": sm[0], "name": sm[1]} for sm in secondary_muscles],
            }
        except Exception as e:
            print(f"[ERROR] get_exercise_by_id: {e}")
            return None

    def update_exercise(self, exercise_id, name, category, equipment, mechanic, force, level, alter_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM exercises WHERE id = %s", (exercise_id,))
                if not cursor.fetchone():
                    conn.close()
                    return False
                cursor.execute("""UPDATE exercises SET name = %s, category = %s, equipment = %s,
                                  mechanic = %s, force = %s, level = %s, alter_id = %s WHERE id = %s""",
                               (name, category, equipment, mechanic, force, level, alter_id, exercise_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] update_exercise: {e}")
            conn.rollback()
            conn.close()
            return False

    def delete_exercise(self, exercise_id):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM exercises WHERE id = %s", (exercise_id,))
                if cursor.rowcount == 0:
                    conn.close()
                    return False
            conn.commit()
            conn.close()
            return True
        except psycopg2.IntegrityError:
            conn.rollback()
            conn.close()
            return False

    def get_most_performed_exercises(self):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("""
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
                """)
                rows = cursor.fetchall()
            conn.close()
            return [{"exercise_id": r[0], "name": r[1], "sports_related": r[2]} for r in rows]
        except Exception as e:
            print(f"[ERROR] get_most_performed_exercises: {e}")
            return []

    def get_exercises_by_muscle(self, muscle):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT DISTINCT e.id, e.name
                    FROM exercises e
                    LEFT JOIN exercise_primary_muscles epm ON e.id = epm.exercise_id
                    LEFT JOIN exercise_secondary_muscles esm ON e.id = esm.exercise_id
                    WHERE LOWER(epm.muscle) = LOWER(%s) OR LOWER(esm.muscle) = LOWER(%s);
                """, (muscle, muscle))
                rows = cursor.fetchall()
            conn.close()
            return [{"exercise_id": r[0], "name": r[1]} for r in rows]
        except Exception as e:
            print(f"[ERROR] get_exercises_by_muscle: {e}")
            return []

    def get_most_complex_exercises(self):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("""
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
                """)
                max_count = cursor.fetchone()[0]
                if max_count is None:
                    conn.close()
                    return []

                cursor.execute("""
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
                """, (max_count,))
                rows = cursor.fetchall()
            conn.close()

            grouped = defaultdict(lambda: {"exercise_id": None, "name": "", "muscle_groups": []})
            for ex_id, name, muscle in rows:
                grouped[ex_id]["exercise_id"] = ex_id
                grouped[ex_id]["name"] = name
                grouped[ex_id]["muscle_groups"].append(muscle)
            return list(grouped.values())
        except Exception as e:
            print(f"[ERROR] get_most_complex_exercises: {e}")
            return []
