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


def generate_random_string(length=16):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

if __name__ == '__main__':

    print(generate_random_string())