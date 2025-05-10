import bcrypt
import psycopg2
from psycopg2.errors import UniqueViolation
from bug_handling.choose_db import get_db_config

class UserDAO:

    def user_exists(self, username, password):
        conn = None
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, password, memory FROM users WHERE username = %s", (username,))
                row = cursor.fetchone()
            conn.close()

            if row and bcrypt.checkpw(password.encode('utf-8'), row[1].encode('utf-8')):
                return row[0], row[2]
            return None, None
        except Exception as e:
            print(f"[ERROR] user_exists: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return None, None

    def create_user(self, username, password, email):
        conn = None
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                print("[DAO] Attempting to create user:", email, username)

                cursor.execute("SELECT 1 FROM users WHERE email = %s", (email,))
                if cursor.fetchone():
                    conn.close()
                    return {"error": "Email already exists."}

                cursor.execute("SELECT 1 FROM users WHERE username = %s", (username,))
                if cursor.fetchone():
                    conn.close()
                    return {"error": "Username already exists."}

                cursor.execute(
                    "INSERT INTO users (email, username, password, memory) VALUES (%s, %s, %s, %s) RETURNING id",
                    (email, username, password, "")
                )
                user_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return {"id": user_id}

        except UniqueViolation:
            if conn:
                conn.rollback()
                conn.close()
            return {"error": "Email or username already exists (DB enforced)."}
        except Exception as e:
            print(f"[ERROR] create_user: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return {"error": "Unexpected error occurred."}

    def insert_memory(self, userid, memory):
        conn = None
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                print(userid)
                cursor.execute(
                    "UPDATE users SET memory = %s WHERE id = %s",
                    (memory, userid)
                )
                success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return success
        except Exception as e:
            print(f"[ERROR] insert_memory: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return None
