import psycopg2

def concept_name_exists(conn, table_name: str, column_name: str, concept_name: str) -> bool:
    with conn.cursor() as cur:
        cur.execute(f"SELECT 1 FROM {table_name} WHERE {column_name} = %s LIMIT 1;", (concept_name,))
        return cur.fetchone() is not None

def get_concept_id(conn, table_name: str, column_name: str, concept_name: str) -> int:
    with conn.cursor() as cur:
        cur.execute(f"SELECT concept_id FROM {table_name} WHERE {column_name} = %s;", (concept_name,))
        result = cur.fetchone()
        return result[0] if result else None