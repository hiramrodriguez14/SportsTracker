import psycopg2
from bug_handling.choose_db import get_db_config

class FragmentDAO:

    def insertFragment(self, did, content, embedding):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO fragments (did, content, embedding)
                    VALUES (%s, %s, %s) RETURNING fid;
                """, (did, content, embedding))
                fid = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return fid
        except Exception as e:
            print(f"[ERROR] insertFragment: {e}")
            conn.rollback()
            conn.close()
            return None

    def getFragments(self, emb):
        try:
            conn = psycopg2.connect(get_db_config().connection_url)
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT DISTINCT did
                    FROM (
                        SELECT did, fid, embedding <-> %s as distance, content
                        FROM fragments
                        ORDER BY distance
                        LIMIT 5
                    ) as subquery
                """, (emb,))
                result = [row[0] for row in cursor.fetchall()]
            conn.close()
            return result
        except Exception as e:
            print(f"[ERROR] getFragments: {e}")
            conn.rollback()
            conn.close()
            return []
