import urllib.request as ur
import json
from django.conf import settings
from payment.celery import app
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task
def get_curse():
    cache_curse = {}

    pairs = ('BTC/USD',
             'ETH/USD',
             'LTC/USD',
             'DASH/USD',
             'BTC/RUR',
             'ETH/RUR',
             'LTC/RUR',
             'DASH/RUR',
             )

    link = 'https://api.livecoin.net/exchange/ticker'
    try:
        byte_json = ur.urlopen(link)
        str_json = json.loads(byte_json.read().decode())
        try:
            if not str_json['success']:
                pass
        except (KeyError, TypeError):
            for i in str_json:
                if i['symbol'] in pairs:
                    cache_curse[i['symbol']] = i['last']
            logger.info('django_json_curse_is_written')
            return cache_curse
    except Exception:
        pass

