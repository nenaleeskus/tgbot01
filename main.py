import telebot
from extensions import CurrencyConverter
from extensions import ConvertException
from config import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.username}.\nЯ умею переводить валюту из одной в другую '
                                      f'по актуальному курсу в определенном количестве.\n'
                                      f'Для этого введи запрос в виде:\n '
                                      f'<из какой валюты> <в какую нужно перевести>\n <и её количество первой>\n '
                                      f'Без ковычек через пробел. \n\nДля вывода доступных валют введи команду /values')


@bot.message_handler(commands=['values'])
def handle_start_help(message):
    bot.send_message(message.chat.id, CurrencyConverter.values())


@bot.message_handler(content_types=['text'])
def reply_to_image(message: telebot.types.Message):
    try:
        data = message.text.lower().split(' ')
        if len(data) != 3:
            raise ConvertException('Введено слишком много параметров.')
        base, quote, amount = data
        bot.send_message(message.chat.id, CurrencyConverter.converter(base, quote, amount))

    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя: \n{e}\n')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду: \n{e}\n')


bot.polling(none_stop=True)
