'''
Бот возвращает цену на определённое количество валюты (евро, доллар или рубль).
При написании бота необходимо использовать библиотеку pytelegrambotapi.
Человек должен отправить сообщение боту в виде <имя валюты, цену которой он хочет узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>.
При вводе команды /start или /help пользователю выводятся инструкции по применению бота.
При вводе команды /values должна выводиться информация о всех доступных валютах в читаемом виде.
Для получения курса валют необходимо использовать API и отправлять к нему запросы с помощью библиотеки Requests.
Для парсинга полученных ответов использовать библиотеку JSON.
При ошибке пользователя (например, введена неправильная или несуществующая валюта или неправильно введено число) вызывать собственно написанное исключение APIException с текстом пояснения ошибки.
Текст любой ошибки с указанием типа ошибки должен отправляться пользователю в сообщения.
Для отправки запросов к API описать класс со статическим методом get_price(), который принимает три аргумента и возвращает нужную сумму в валюте:
- имя валюты, цену на которую надо узнать, — base;
- имя валюты, цену в которой надо узнать, — quote;
- количество переводимой валюты — amount.
Токен Telegram-бота хранить в специальном конфиге (можно использовать .py файл).
Все классы спрятать в файле extensions.py.
'''

import requests
import telebot
import json

TOKEN = '5352983388:AAFtZEqNJoHrmDxBYrguFoSlycTdiYGp5_E'

keys = {
    'белруб': 'BYN',
    'русруб': 'RUB',
    'еуро': 'EUR',
    'бакс': 'USD',
    'злотый': 'PLN',
    'йена': 'JPY',
    'биткоин': 'BTC',
    'эфириум': 'ETH',
}

bot = telebot.TeleBot(TOKEN)


class Conver_Exeption(Exception):
    pass

@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.reply_to(message, "Вас приветствует бот конвертации валют! Нажмите /help для справки")

@bot.message_handler(commands = ['help'])
def send_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боты в следующем формате:\n' \
           '<имя валюты>' \
           '<в какую валюту перевести>' \
           '<колличество переводимой валюты>\n' \
           'Список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def send_values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    text = text + '\n'.join(keys)
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text'])
def convers(message: telebot.types.Message):
    items = message.text.split(' ')

    # if len(items) != 2 and len(items) != 3:
    #     raise Conver_Exeption(f'Не верное колличество входных данных')
    if len(items) == 2:
        amount = 1
        quote, base = items
    elif len(items) == 3:
        quote, base, amount = items
    else:
        raise Conver_Exeption(f'Неверное колличество входных данных')

    quote, base = quote.lower(), base.lower()

    if quote not in keys:
        raise Conver_Exeption(f'Такой валюты {quote} нет в списке доступных')
    if base not in keys:
        raise Conver_Exeption(f'Такой валюты {base} нет в списке доступных')
    if not str(amount).isnumeric():
        raise Conver_Exeption(f'{amount} не является числом')

    cur = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
    one = json.loads(cur.content)[keys[base]]
    all_cur = one * int(amount)
    text = f'За {amount} {quote} дадут {all_cur} {base}'
    bot.send_message(message.chat.id, text)


bot.infinity_polling()
# bot.polling()
