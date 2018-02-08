import urllib.request as ur
import json
from django.conf import settings
from payment.celery import app
from celery.utils.log import get_task_logger
import time

logger = get_task_logger(__name__)
redis = getattr(settings, 'CACHE_REDIS', None)


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

    link = 'https://api.coinmarketcap.com/v1/ticker'
    link2 = 'https://api.coinmarketcap.com/v1/ticker/?convert=RUB'
    byte_json = ur.urlopen(link)
    byte_json2 = ur.urlopen(link2)
    str_json = json.loads(byte_json.read().decode())
    str_json2 = json.loads(byte_json2.read().decode())
    if str_json and str_json2:
        redis.flushall()
        for i in str_json:
            pair = i['symbol'] + '/USD'
            if pair in pairs:
                cache_curse[pair] = i['price_usd']
        for i in str_json2:
            pair = i['symbol'] + '/RUR'
            if pair in pairs:
                cache_curse[pair] = i['price_rub']

        logger.info('django_json_curse_is_written')
        cache_curse['time'] = time.time()
        return cache_curse

