import os
import re
import string
import random

from decimal import Decimal as D

# round_down = lambda amount: D(str(amount)).quantize(D('.01'), rounding='ROUND_DOWN')
# round_up = lambda amount: D(str(amount)).quantize(D('.01'), rounding='ROUND_UP')
format_amount = lambda amount: format(round_down(amount), '.2f')

round_up = lambda (amount): (D(str(amount))).to_integral_value('ROUND_HALF_UP')
round_down = lambda (amount) : (D(str(amount))).to_integral_value('ROUND_DOWN')

def extract_string(regex, test_string):
    try:
        return re.search(regex, test_string).groups()[0]
    except IndexError:
        return test_string

#----------------------
def generate_random_password(length=15):
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))

    return ''.join(random.choice(chars) for i in range(length))

def generate_random_code(limit, possible_chars):
    return ''.join(random.choice(possible_chars) for i in range(limit))

def generate_alphanumeric_code(limit=10):
    return generate_random_code(limit, possible_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")

def generate_random_number(limit=10):
    return generate_random_code(limit, possible_chars="1234567890")

def get_account_no(limit=8):
    return generate_random_number(limit)

def get_reference_no(limit=8):
    return generate_alphanumeric_code(limit)
#----------------------

SAFARICOM_PHONE_REGEX = r"^(\+2547|07)(?P<prefix>(([0-2]|[9])[0-9]))(?P<postfix>\d{6})$"
VALID_SAFARICOM_NO_REGEX = SAFARICOM_PHONE_REGEX 
MOBILE_PHONE_REGEX = r"^(\+2547|07)(?P<prefix>([0-9][0-9]))(?P<postfix>\d{6})$"
def clean_phone_no(phone_no):
    phone_no = phone_no or ''

    if re.match(MOBILE_PHONE_REGEX, phone_no):
        return phone_no

    if phone_no.startswith('07'):
        return clean_phone_no("+2547%s" % phone_no[2:])

    if phone_no.startswith('7'):
        return clean_phone_no("+254%s" % phone_no)

    if phone_no.startswith('2547'):
        return clean_phone_no("+%s" % phone_no)

    if phone_no.startswith('25407'):
        return clean_phone_no("+254%s" % phone_no[4:])

    if phone_no.startswith('+25407'):
        return clean_phone_no("+254%s" % phone_no[5:])
        
def clean_safaricom_no(phone_no):
    phone_no = clean_phone_no(phone_no)

    if phone_no is not None and re.match(SAFARICOM_PHONE_REGEX, phone_no):
        return phone_no