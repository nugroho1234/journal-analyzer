import random
import string
import tiktoken

def count_tokens(text, model="gpt-4o"):
    # Load the tokenizer
    enc = tiktoken.encoding_for_model(model)
    
    # Encode the text
    tokens = enc.encode(text)
    
    # Return the number of tokens
    return len(tokens)


def generate_random_string(first_three_chars: str, length: int = 16) -> str:
    if len(first_three_chars) != 3:
        raise ValueError("The input must be exactly 3 characters long.")
    
    characters = string.ascii_letters + string.digits
    remaining_length = length - 3
    random_string = ''.join(random.choice(characters) for _ in range(remaining_length))
    return first_three_chars + random_string

def id_exists_in_db(conn, 
                    table_name: str, 
                    id_column: str, 
                    id_value: str) -> bool:
    with conn.cursor() as cur:
        cur.execute(f"SELECT 1 FROM {table_name} WHERE {id_column} = %s LIMIT 1;", (id_value,))
        return cur.fetchone() is not None

def generate_unique_id(conn, table_name: str, id_column: str, first_three_chars: str, length: int = 16) -> str:
    while True:
        new_id = generate_random_string(first_three_chars, length)
        if not id_exists_in_db(conn, table_name, id_column, new_id):
            return new_id

if __name__ == '__main__':

    print(generate_unique_id('CON'))