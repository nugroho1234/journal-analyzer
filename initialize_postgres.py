import psycopg2
import os
from dotenv import load_dotenv


def print_table_names(dbname:str,
                      user:str,
                      password:str,
                      host:str):
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute a query
        # Execute a query to get the table names
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """)

        # Retrieve query results
        tables = cur.fetchall()

        # Print the table names
        print("Tables in the database:")
        for table in tables:
            print(table[0])

        # Close the cursor and connection
        cur.close()
        conn.close()


    except Exception as error:
        print("Error while connecting to PostgreSQL", error)


def delete_table(dbname:str,
                user:str,
                password:str,
                host:str,
                table:str):
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(
            dbname="journal_analyzer_database",
            user="agusnug",
            password="danifiltH7!1985",
            host="localhost"
            )
        cur = conn.cursor()
        cur.execute(f'DROP TABLE IF EXISTS {table} CASCADE;')

        conn.commit()
        cur.close()
        conn.close()
    except Exception as error:
        print(error)

if __name__ == '__main__':
    load_dotenv()
    dbname = os.getenv('POSTGRES_DBNAME')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = 'localhost'
    print_table_names(dbname, user, password, host)
    delete_table(dbname, user, password, host, 'langchain_pg_embedding')
    print_table_names(dbname, user, password, host)
