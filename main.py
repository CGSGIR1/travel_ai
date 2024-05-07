import telebot
import os.path
from telebot import types
import gis, settings
bot = telebot.TeleBot('7131622872:AAExYrKxu4Fw3z9wyLbxEpk-oZgkdwd6XRY')
fl=0
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Построить маршрут")
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     text="Добро пожаловать в бот для построения маршрутов".format(
                         message.from_user),reply_markup=markup)

def ret(a,b,c):
    print(a,b,c)

@bot.message_handler(content_types=['text'])
def func(message):
    global fl
    if (message.text == "Построить маршрут"):
        hideBoard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton("На авто")
        btn4 = types.KeyboardButton("Пешком")
        btn5 = types.KeyboardButton("На жд")
        hideBoard.add(btn3,btn4,btn5)
        bot.send_message(message.chat.id, text="Выберите вид транспорта:",reply_markup=hideBoard)
    elif (message.text == "На авто"):
        fl=1
        hideBoard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton("В главное меню📱")
        hideBoard.add(btn3)
        bot.send_message(message.chat.id, text="Введите Город отправления и прибытия в формате: Город1, Город2",reply_markup=hideBoard)
    elif (message.text == "Пешком"):
        fl=2
        hideBoard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton("В главное меню📱")
        hideBoard.add(btn3)
        bot.send_message(message.chat.id, text="Введите Город отправления и прибытия в формате: Город1, Город2",reply_markup=hideBoard)
    elif (message.text == "На жд"):
        fl=3
        hideBoard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton("В главное меню📱")
        hideBoard.add(btn3)
        bot.send_message(message.chat.id, text="Введите Город отправления и прибытия в формате: Город1, Город2",reply_markup=hideBoard)
    elif (message.text == "В главное меню📱"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Построить маршрут")
        markup.add(btn1)
        bot.send_message(message.chat.id,
                         text="Добро пожаловать в бот для построения маршрутов".format(
                             message.from_user), reply_markup=markup)
    elif (message.text == "2Gis"):
        result = gis.PublicTransport(settings.gis_public_transport_url)
        bot.send_message(message.chat.id,
                         text=result.text[:50])
    elif fl!=0:
        s=str(message.text)
        try:
            s2=list(map(str,s.split(", ")))
            result = gis.PublicTransport(settings.gis_public_transport_url, s2[0], s2[1])
        except:
            bot.send_message(message.chat.id,
                             text="Неправильный формат данных. Введите снова".format(
                                 message.from_user))
    else:
        bot.send_message(message.chat.id, text="Неверный формат сообщения")
bot.polling(none_stop=True)
