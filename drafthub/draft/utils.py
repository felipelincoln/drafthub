import random
import string


CHAR_STRING = string.ascii_lowercase + string.digits

def generate_random_string(chars=CHAR_STRING, size=6):
    return ''.join(random.choice(chars) for _ in range(size))
