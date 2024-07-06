import psycopg2
import os

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
            dbname=dbname,
            user=user,
            password=password,
            host=host
            )
        cur = conn.cursor()
        cur.execute(f'DROP TABLE IF EXISTS {table} CASCADE;')

        conn.commit()
        cur.close()
        conn.close()
    except Exception as error:
        print(error)

def check_table_exists(dbname:str, 
                       user:str, 
                       password:str, 
                       host:str, 
                       table_name:str):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        cursor = conn.cursor()

        check_table_query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = %s
        );
        """
        cursor.execute(check_table_query, (table_name,))
        table_exists = cursor.fetchone()[0]
    except psycopg2.Error as e:
        print(f"Error checking table existence: {e}")
        return False  # Or raise an exception, depending on your needs
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return table_exists

def create_table(dbname:str, 
                 user:str, 
                 password:str, 
                 host:str, 
                 query:str):
    try:
        with psycopg2.connect(dbname=dbname, user=user, password=password, host=host) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
            conn.commit()
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        raise  # Re-raise the exception after logging (optional)

def check_and_create_table(dbname:str, 
                           user:str, 
                           password:str, 
                           host:str, 
                           table_name:str, 
                           query:str):
    table_exists = check_table_exists(dbname, user, password, host, table_name)
    if not table_exists:
        create_table(dbname, user, password, host, query)
        print(f"Table '{table_name}' created successfully.")
    else:
        print(f"Table '{table_name}' already exists. Skipping creation.")

def create_index(dbname:str, 
                user:str, 
                password:str, 
                host:str):   
    # Connect to the PostgreSQL database
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        cursor = conn.cursor()
        
        # Create the index
        create_index_query = """
        CREATE INDEX idx_definitions_concept_id ON definitions(concept_id);
        CREATE INDEX idx_definitions_article_id ON definitions(article_id);
        """
        
        cursor.execute(create_index_query)
        
        # Commit the transaction
        conn.commit()
        
        print("Indices created successfully")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        conn.close()
