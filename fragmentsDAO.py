from bug_handling.choose_db import get_db_config
import psycopg2

class FragmentDAO:
    
  def __init__(self):
        self.conn = psycopg2.connect(get_db_config().connection_url)
        
  def insertFragment(self, did, content, embedding):
      cursor = self.conn.cursor()
      query = """
      INSERT INTO fragments (did, content, embedding) values (%s, %s, %s) RETURNING fid;
      """
      cursor.execute(query,(did, content, embedding))
      fid = cursor.fetchone()[0]
      self.conn.commit()
      cursor.close()
      return fid
  
  def getFragments(self, emb):
    cursor = self.conn.cursor()
    query = """
    SELECT did, fid, distance, content 
    FROM (
        SELECT did, fid, embedding <-> %s as distance, content 
        FROM fragments 
        ORDER BY distance
        LIMIT 5
    ) as subquery
    """
    cursor.execute(query, (emb,))
    result = []
    for row in cursor:
        result.append(row)
    return result
