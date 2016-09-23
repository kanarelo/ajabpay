import os
import re
import string
import random

def extract_string(regex, test_string):
    try:
        return re.search(regex, test_string).groups()[0]
    except IndexError:
        return test_string

def generate_random_password(length=15):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))

def get_reference_no(limit=10):
    possible_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    chosen_chars = ""
    z = 0

    while (z <= limit):
        chosen_chars = (chosen_chars + random.choice(possible_chars))
        z += 1

    return chosen_chars
