import telebot
from config import TELEGRAM_TOKEN, keys
from extensions import APIException, CryptoConverter, choose_plural

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Для выполнения расчета введите строку в следующем формате (через один пробел): \n\n" \
           "валюта_№1  валюта_№2  сумма_валюты_№1\n\n" \
           "Пример: доллар евро 10 \n\n" \
           "Список доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: \n'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        message_words = message.text.split(' ')
        if len(message_words) != 3:
            raise APIException('Неверный формат ввода.\n\nДля справки нажмите /start')

        base, quote, amount = message_words
        amount = amount.replace(',', '.')
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f"{choose_plural(amount, base)} = {choose_plural(total_base, quote)}."
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
