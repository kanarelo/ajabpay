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

def get_reference_no(limit=10, 
    possible_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"):

    return ''.join(random.choice(possible_chars) for i in range(limit))

def get_account_no(limit=8):
    return get_reference_no(possible_chars="1234567890")