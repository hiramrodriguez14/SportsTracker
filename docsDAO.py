from bug_handling.choose_db import get_db_config
import psycopg2

class DocumentDAO:
    
  def __init__(self):
        self.conn = psycopg2.connect(get_db_config().connection_url)
        
  def insertDocument(self, docname):
      cursor = self.conn.cursor()
      query = """
      INSERT INTO docs (docname) values (%s) RETURNING did;
      """
      cursor.execute(query,(docname,))
      did = cursor.fetchone()[0]
      self.conn.commit()
      cursor.close()
      return did
  
