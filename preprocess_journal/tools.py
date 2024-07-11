import random
import string
import tiktoken
import os
import shutil

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


def move_files_to_tmp(source_folder:str = "unfinished/Articles",
                      destination_folder:str = "tmp/Articles"):
    # Create the destination folder if it does not exist
    os.makedirs(destination_folder, exist_ok=True)

    # Copy all files from the source to the destination folder
    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename)
        destination_file = os.path.join(destination_folder, filename)
        
        # Check if it is a file (not a directory)
        if os.path.isfile(source_file):
            shutil.copy2(source_file, destination_file)

    # Delete all files in the source folder
    for filename in os.listdir(source_folder):
        source_file = os.path.join(source_folder, filename)
        
        # Check if it is a file (not a directory) and delete it
        if os.path.isfile(source_file):
            os.remove(source_file)

    print("Files copied and original files deleted.")

def move_one_file(source_folder, destination_folder, filename):
    # Ensure the source file exists
    source_file = os.path.join(source_folder, filename)
    if not os.path.isfile(source_file):
        raise FileNotFoundError(f"The file {filename} does not exist in the source folder.")
    
    # Create the destination folder if it does not exist
    os.makedirs(destination_folder, exist_ok=True)

    # Define the destination file path
    destination_file = os.path.join(destination_folder, filename)

    # Move the file
    shutil.move(source_file, destination_file)
    print(f"Moved {filename} to {destination_folder}")

if __name__ == '__main__':

    print(generate_unique_id('CON'))