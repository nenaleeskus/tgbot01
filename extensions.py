import json
import requests
from config import API_KEY
keys = {
    "рубль": "RUB",
    "доллар": "USD",
    "евро": "EUR"
}


class ConvertException(Exception):
    pass


class CurrencyConverter:  # Основной класс обработки полученной информации (отправка запроса и получение) и проверки
    # исключений
    @staticmethod
    def converter(base, quote, amount):
        global keys
        try:
            quote = keys[quote]
        except KeyError:
            raise ConvertException(f'Не удалось обработать параметр {quote}, введите доступную валюту')
        try:
            base = keys[base]
        except KeyError:
            raise ConvertException(f'Не удалось обработать параметр {base}, введите доступную валюту')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'не удалось обработать {amount}')
        if quote == base:
            raise ConvertException('Введены одинаковые валюты.')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={quote}&from={base}&amount={amount}"
        payload = {}
        headers = {
            "apikey": API_KEY
        }
        response = requests.request("GET", url, headers=headers, data=payload)      # взято из документации на сайте API
        result = response.text
        data = json.loads(result)
        return f"{data['result']} {data['query']['to']}"

    @staticmethod
    def values():  # Метод вывода списка доступных валют
        text = 'Список доступных валют:'
        global keys
        for key in keys.keys():
            text = '\n· '.join((text, key))
        return text
