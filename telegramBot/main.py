# -*- coding: utf-8 -*-
#
# main.py from telegramBot
# version = 0.1
# For skillfactory B10.6
import telebot
from extensions import APIException, BotConverter, keys, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    text = 'Переведу из первой валюты во вторую валюту в указанном количестве.\
           \n/values покажет доступные валюты'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler()
def conversion(message: telebot.types.Message):
    try:
        value = message.text.split(' ')
        if len(value) < 3:
            raise APIException('Должно быть хотя бы 3 параметра')
        quote, base, amount = value[:3]
        total_base = BotConverter.get_price(quote, base, amount)
    except APIException as er:
        bot.reply_to(message, f'Ошибка в пользовательской команде:\n{er}')
    except Exception as er:
        bot.reply_to(message, f'Не удалось исполнить команду:\n{er}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
