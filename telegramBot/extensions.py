# -*- coding: utf-8 -*-
#
# extensions.py from telegramBot
# version = 0.1
# For skillfactory B10.6
import requests
import json

TOKEN = "5732531504:AAELA0vwzghbUstpu-0R85N3a6QKeKZmNvQ"
HEADER = {'apikey': 'xaQdJKR29EppP26DxijToWnpNsHiABQY'}
keys = {'евро': 'EUR',
        'рубль': 'RUB',
        'доллар': 'USD'}


class APIException(Exception):
    pass


class BotConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('Валюты должны быть разными')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не известная валюта: {quote} ')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не известная валюта: {base} ')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Количество не выражается числом: {amount} ')

        r = requests.get(f'https://api.apilayer.com/fixer/convert?from={quote_ticker}&to={base_ticker}&amount={amount}',
                         headers=HEADER)
        total_base = json.loads(r.content)['result']

        return total_base
