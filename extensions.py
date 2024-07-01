from config import keys
import requests


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        quote = quote.lower()
        base = base.lower()
        if quote == base:
            raise APIException(f'Введите различные валюты, Вы ввели 2 раза {base}.')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Валюта {base} не доступна из списка валют.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Валюта {quote} не доступна из списка валют.')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: {amount}.\nПроверьте введенные данные.')
        if int(amount) <= 0:
            raise APIException("Сумма должна быть больше 0.")

        response = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")
        total_base = response.json().get(keys[quote]) * amount
        return total_base


def choose_plural(initial_amount, currency: str):
    initial_amount = float(initial_amount)
    amount = int(initial_amount)
    currency = currency.lower()
    variants, variant = (), 0
    if amount % 10 == 1 and amount % 100 != 11:
        variant = 0
    elif 2 <= amount % 10 <= 4 and (amount % 100 < 10 or amount % 100 >= 20):
        variant = 1
    else:
        variant = 2

    if currency == 'доллар':
        variants = ('доллар', 'доллара', 'долларов')
    elif currency == 'рубль':
        variants = ('рубль', 'рубля', 'рублей')
    elif currency == 'евро':
        variants = ('евро', 'евро', 'евро')
    return f"{initial_amount:.2f} {variants[variant]}"
