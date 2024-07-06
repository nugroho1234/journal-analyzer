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


def generate_random_string(first_three_chars:str, 
                           length:int=16):
    if len(first_three_chars) != 3:
        raise ValueError("The input must be exactly 3 characters long.")
    
    characters = string.ascii_letters + string.digits
    remaining_length = length - 3
    random_string = ''.join(random.choice(characters) for _ in range(remaining_length))
    return first_three_chars + random_string

if __name__ == '__main__':

    print(generate_random_string('CON'))