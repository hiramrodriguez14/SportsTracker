import psycopg2
from app.config.pgconfig import pgconfig

class FixIdTool:
    def __init__(self):
        url = "dbname=%s password=%s host=%s port=%s user=%s" % (
            pgconfig.DB_NAME,
            pgconfig.DB_PASSWORD,
            pgconfig.DB_HOST,
            pgconfig.DB_PORT,
            pgconfig.DB_USER
        )
        self.conn = psycopg2.connect(url)

    def reset_sequence(self, table, id_column='id'):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                f"SELECT setval(pg_get_serial_sequence('{table}', '{id_column}'), (SELECT MAX({id_column}) FROM {table}));"
            )
            self.conn.commit()
            print(f"Sequence for '{table}' reset successfully.")
        except Exception as e:
            print(f"Error resetting sequence: {e}")
        finally:
            cursor.close()
            self.conn.close()

if __name__ == "__main__":
    table_name = input("Enter the name of the table to reset the sequence for: ").strip()
    tool = FixIdTool()
    tool.reset_sequence(table_name)
