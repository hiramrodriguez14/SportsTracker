import psycopg2
from bug_handling.choose_db import get_db_config

class DocumentDAO:

    def insertDocument(self, docname, content):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO docs (docname, content) VALUES (%s, %s) RETURNING did;", (docname, content))
                did = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return did
        except Exception as e:
            print(f"[ERROR] insertDocument: {e}")
            conn.rollback()
            conn.close()
            return None

    def getDocuments(self, did_list):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT did, docname, content
                    FROM docs
                    WHERE did = ANY(%s);
                """, (did_list,))
                rows = cursor.fetchall()
            conn.close()
            return {row[0]: {"docname": row[1], "content": row[2]} for row in rows}
        except Exception as e:
            print(f"[ERROR] getDocuments: {e}")
            conn.rollback()
            conn.close()
            return {}
