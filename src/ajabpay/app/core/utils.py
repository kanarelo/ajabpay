import random

def get_reference_no(limit=10):
    possible_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    chosen_chars = ""
    z = 0

    while (z <= limit):
        chosen_chars = (chosen_chars + random.choice(possible_chars))
        z += 1

    return chosen_chars
