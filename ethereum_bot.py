import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask import Flask, jsonify
from flask_mail import Mail

import config
from ethereum_service import EthereumService

app = Flask(__name__)
app.config.from_object(config)
mail = Mail(app)
ethereum_service = EthereumService()

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=ethereum_service.get_eth_price,
    trigger=IntervalTrigger(seconds=5),
    id='price_job',
    name='Print ethereum spot price every five seconds',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


@app.route('/')
def hello_world():
    return 'Amedviediev ethereum bot is online'


@app.route('/api/v1/price/eth')
def current_price():
    spot = ethereum_service.get_eth_price()
    return jsonify(spot)


if __name__ == '__main__':
    app.run()
