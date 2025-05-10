import psycopg2

# este archivo 
DB_NAME = "dfqftn892u378j"
DB_USER = "u5ie5npmv1rgvf"
DB_PASSWORD = "p5167c9c6edb4adfcd313ff0d0b54c4cc526b38ab65f3fdf9e9b704a6fe397473"
DB_HOST = "cd1goc44htrmfn.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com"
DB_PORT = "5432"

def connect_and_list_tables():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            sslmode='require'
        )
        cursor = conn.cursor()

        cursor.execute("SELECT current_database();")
        dbname = cursor.fetchone()[0]
        print(f"\nConnected to database: {dbname}\n")

        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema='public' AND table_type='BASE TABLE';
        """)
        tables = cursor.fetchall()

        if tables:
            print("Tables in the database:")
            for table in tables:
                print(f" - {table[0]}")
        else:
            print("No tables found in this database.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"[ERROR] Could not connect to the database:\n{e}")

if __name__ == "__main__":
    connect_and_list_tables()
