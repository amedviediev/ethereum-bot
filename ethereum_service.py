import datetime
import os

from coinbase.wallet.client import Client
from coinbase.wallet.model import APIObject
from flask_mail import Message

from config import ADMINS
from decorators import async


class EthereumService:

    low_price = 250
    low_price_triggered = False

    def get_eth_price(self):
        client = Client(os.environ.get('COINBASE_KEY'), os.environ.get('COINBASE_SECRET'), api_version='2017-05-26')
        # rates = client.get_spot_price(currency_pair='ETH-USD')
        spot = client._make_api_object(client._get('v2', 'prices', 'ETH-USD', 'spot'), APIObject)

        current_time = datetime.datetime.utcnow().strftime("%a %b %d %Y %H:%M:%S UTC")
        print('{} ETH price is {}'.format(current_time, spot.amount))

        self.check_buy_price(spot.amount)
        return spot

    def check_buy_price(self, price):
        if float(price) < self.low_price and self.low_price_triggered is False:
            print('Price is under limit, time to buy')
            self.low_price_triggered = True
            # self.send_async_email()
        elif float(price) > self.low_price and self.low_price_triggered is True:
            self.low_price_triggered = False

    @async
    def send_async_email(self):
        msg = Message('test subject', sender=ADMINS[0], recipients=ADMINS)
        msg.body = 'text body'
        msg.html = '<b>HTML</b> body'

        from ethereum_bot import app, mail

        with app.app_context():
            mail.send(msg)
