import paypalrestsdk
from decimal import Decimal as D

ENDPOINT = "http://localhost:5000"

PAYPAL_MODE = "sandbox"
PAYPAL_CLIENT_ID = "ATo_Io1R9XCX9SmfHdGbeXYSKZnireDROhLUwcjO_VtLiUx7yB7CuMjTWJO0JgfGSXhxCLsLXna3KIn0"
PAYPAL_CLIENT_SECRET = "EIbbidsOH9Y_2aXPiInRs7Wf-2Emn6fBzTfHXjxgZwC23Lu00zhvA2rImcz-7nkr1OfaDNuwq4yUWgYV"

round_down = lambda amount: D(str(amount)).quantize(D('.01'), rounding='ROUND_DOWN')
round_up = lambda amount: D(str(amount)).quantize(D('.01'), rounding='ROUND_UP')
format_amount = lambda amount: format(round_down(amount), '.2f')

def create_paypalrestsdk_api():
    return paypalrestsdk.Api({
        "mode": PAYPAL_MODE,
        "client_id": PAYPAL_CLIENT_ID,
        "client_secret": PAYPAL_CLIENT_SECRET 
    })
