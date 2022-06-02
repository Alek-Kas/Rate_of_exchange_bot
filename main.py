'''Бот возвращает цену на определённое количество валюты (евро, доллар или рубль). При написании бота необходимо
использовать библиотеку pytelegrambotapi. Человек должен отправить сообщение боту в виде <имя валюты, цену которой он
хочет узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>. При вводе команды
/start или /help пользователю выводятся инструкции по применению бота. При вводе команды /values должна выводиться
информация о всех доступных валютах в читаемом виде. Для получения курса валют необходимо использовать API и
отправлять к нему запросы с помощью библиотеки Requests. Для парсинга полученных ответов использовать библиотеку
JSON. При ошибке пользователя (например, введена неправильная или несуществующая валюта или неправильно введено
число) вызывать собственно написанное исключение APIException с текстом пояснения ошибки. Текст любой ошибки с
указанием типа ошибки должен отправляться пользователю в сообщения. Для отправки запросов к API описать класс со
статическим методом get_price(), который принимает три аргумента и возвращает нужную сумму в валюте: - имя валюты,
цену на которую надо узнать, — base; - имя валюты, цену в которой надо узнать, — quote; - количество переводимой
валюты — amount. Токен Telegram-бота хранить в специальном конфиге (можно использовать .py файл). Все классы спрятать
в файле extensions.py. '''


import telebot

from my_token import TOKEN
from extensions import ConverExeption, Converter, Curen
from config import keys

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Вас приветствует бот конвертации валют! Нажмите /help для справки")


@bot.message_handler(commands=['help'])
def send_help(message: telebot.types.Message):
    # text = 'Чтобы начать работу введите комманду боту в следующем формате:\n' \
    #        '<имя валюты>' \
    #        ' <в какую валюту перевести>' \
    #        ' <колличество переводимой валюты>\n' \
    #        'Список всех доступных валют: /values'
    text = 'Что бы сконвертировать одну валюту в другую, выберите валюту из списка. ' \
           'Затем выберите валюту в которую хотите перевести. ' \
           'После этого введите колличество валюты для конвертации.\n' \
           'Начать конвертацию - /values\n'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def send_values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    text = text + '\n'.join(keys)
    bot.reply_to(message, text)
    bot.register_next_step_handler(message, add_base)
    # print(base)
def add_base(message):
    Curen.base = message.text[1:4]
    bot.register_next_step_handler(message, add_quote)
    # return base
def add_quote(message):
    Curen.quote = message.text[1:4]
    bot.register_next_step_handler(message, add_amount)
def add_amount(message):
    Curen.amount = message.text
    # print(curen.base, curen.quote, curen.amount)
    # print(self.base, self.quote, self.amount)
    try:
        total_cost = Converter.get_price(Curen.quote, Curen.base, Curen.amount)
    except ConverExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'За {Curen.amount} {Curen.quote} дадут {total_cost} {Curen.base}'
        bot.send_message(message.chat.id, text)


# @bot.message_handler(content_types=['text'])
# def convers(message: telebot.types.Message):
#     try:
#         items = message.text.split(' ')
#         if len(items) == 2:  # Если колличество не введено - считать колличество = 1
#             amount = 1
#             quote, base = items
#         elif len(items) == 3:
#             quote, base, amount = items
#         else:
#             raise ConverExeption(f'Неверное колличество входных данных')
#         quote, base = quote.lower(), base.lower()
#         total_cost = Converter.get_price(quote, base, amount)
#     except ConverExeption as e:
#         bot.reply_to(message, f'Ошибка пользователя\n{e}')
#     except Exception as e:
#         bot.reply_to(message, f'Не удалось обработать команду\n{e}')
#     else:
#         text = f'За {amount} {quote} дадут {total_cost} {base}'
#         bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling()
    # bot.infinity_polling()  # бесконечный бот
