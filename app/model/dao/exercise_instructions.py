import psycopg2
from bug_handling.choose_db import get_db_config

class ExerciseInstructionsDAO:

    def exerciseExists(self, eid):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM exercises WHERE id = %s", (eid,))
                result = cursor.fetchone() is not None
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] exerciseExists: {e}")
            conn.rollback()
            conn.close()
            return False

    def instructionExists(self, insid):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM exercise_instructions WHERE id = %s", (insid,))
                result = cursor.fetchone() is not None
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] instructionExists: {e}")
            conn.rollback()
            conn.close()
            return False

    def isNotValidInstructionNumber(self, exercise_id, num):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM exercise_instructions WHERE exercise_id = %s AND instruction_number = %s",
                    (exercise_id, num)
                )
                result = cursor.fetchone() is not None
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] isNotValidInstructionNumber: {e}")
            conn.rollback()
            conn.close()
            return False

    def insertExerciseInstruction(self, eid, num, instr):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO exercise_instructions (exercise_id, instruction_number, instruction) VALUES (%s, %s, %s) RETURNING id",
                    (eid, num, instr)
                )
                inserted_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return inserted_id
        except Exception as e:
            print(f"[ERROR] insertExerciseInstruction: {e}")
            conn.rollback()
            conn.close()
            return None

    def deleteExerciseInstruction(self, eid, insid):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM exercise_instructions WHERE exercise_id = %s AND id = %s",
                    (eid, insid)
                )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"[ERROR] deleteExerciseInstruction: {e}")
            conn.rollback()
            conn.close()
            return False
