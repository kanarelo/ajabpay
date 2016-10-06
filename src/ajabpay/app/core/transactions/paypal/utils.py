from decimal import Decimal as D

from ajabpay.index import app

round_down = lambda amount: D(str(amount)).quantize(D('.01'), rounding='ROUND_DOWN')
round_up = lambda amount: D(str(amount)).quantize(D('.01'), rounding='ROUND_UP')
format_amount = lambda amount: format(round_down(amount), '.2f')