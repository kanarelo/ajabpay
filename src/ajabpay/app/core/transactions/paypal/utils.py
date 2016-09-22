import paypalrestsdk
from decimal import Decimal as D

from ajabpay.config import BaseConfig

round_down = lambda amount: D(str(amount)).quantize(D('.01'), rounding='ROUND_DOWN')
round_up = lambda amount: D(str(amount)).quantize(D('.01'), rounding='ROUND_UP')
format_amount = lambda amount: format(round_down(amount), '.2f')

def create_paypalrestsdk_api():
    return paypalrestsdk.Api(dict(
        mode=BaseConfig.PAYPAL_MODE,
        client_id=BaseConfig.PAYPAL_CLIENT_ID,
        client_secret=BaseConfig.PAYPAL_CLIENT_SECRET
    ))
