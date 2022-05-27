import requests
import json

from config import keys


class ConverExeption(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote=str, base=str, amount=str):
        try:
            quote_key = keys[quote]
        except KeyError:
            raise ConverExeption(f'Такой валюты {quote} нет в списке доступных')
        try:
            base_key = keys[base]
        except KeyError:
            raise ConverExeption(f'Такой валюты {base} нет в списке доступных')
        try:
            amount = float(amount)
        except ValueError:
            raise ConverExeption(f'{amount} не является числом')
        # if quote_key == base_key:
        try:
            assert quote_key != base_key
        except AssertionError:
            raise ConverExeption(f'{quote} и {base} одна и та же валюта')

        cur = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_key}&tsyms={base_key}')
        one = json.loads(cur.content)[base_key]
        multiply_cur = one * amount
        return multiply_cur
