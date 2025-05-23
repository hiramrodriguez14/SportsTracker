import psycopg2
from bug_handling.choose_db import get_db_config

class ExerciseInstructionsDAO:
    def __init__(self):
        self.conn = psycopg2.connect(get_db_config().connection_url)

    def exerciseExists(self, eid):
        cursor = self.conn.cursor()
        query = "SELECT 1 FROM exercises WHERE id = %s"
        cursor.execute(query, (eid,))
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def instructionExists(self, insid):
        cursor = self.conn.cursor()
        query = "SELECT 1 FROM exercise_instructions WHERE id = %s"
        cursor.execute(query, (insid,))
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def isNotValidInstructionNumber(self, exercise_id, num):
        cursor = self.conn.cursor()
        query = "SELECT 1 FROM exercise_instructions WHERE exercise_id = %s AND instruction_number = %s"
        cursor.execute(query, (exercise_id, num))
        exists = cursor.fetchone() is not None
        cursor.close()
        return exists

    def insertExerciseInstruction(self, eid, num, instr):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO exercise_instructions (exercise_id, instruction_number, instruction) VALUES (%s, %s, %s) returning id",
            (eid, num, instr)
        )
        id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return id

    def deleteExerciseInstruction(self, eid, insid):
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM exercise_instructions WHERE exercise_id = %s AND id = %s",
            (eid, insid)
        )
        self.conn.commit()
        cursor.close()
        return
