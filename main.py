import telebot
import os.path
from telebot import types
import gis, settings
from testik import GptAnswer
from ModelLoad import GigachatStart, AIResponse
from CreateEmbeddings import CreateEmbeddings
import logging

logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(settings.telebot_token)
active_sessions = dict()
CreateEmbeddings()
GigaChat, GigaRet = GigachatStart()
logging.info("ГигаЧат загрузили")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Построить маршрут")
    btnGuide = types.KeyboardButton("Пообщаться с гидом")
    markup.add(btnGuide)
    markup.add(btn1)
    active_sessions[message.chat.id] = 0
    bot.send_message(message.chat.id,
                     text="Добро пожаловать в бот для построения маршрутов".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global active_sessions
    try:
        zashita = active_sessions[message.chat.id]
    except:
        active_sessions[message.chat.id] = 0
    if (message.text == "Построить маршрут"):
        hideBoard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton("Прямой")
        btn4 = types.KeyboardButton("Экскурсионный")
        hideBoard.add(btn3, btn4)
        bot.send_message(message.chat.id, text="Выберите тип маршрута:", reply_markup=hideBoard)
    elif (message.text == "Пообщаться с гидом"):
        hideBoard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mainMenuBtn = types.KeyboardButton("В главное меню📱")
        hideBoard.add(mainMenuBtn)
        bot.send_message(message.chat.id,
                         text="Здравствуйте! Я рада, что вы заинтересовались моими услугами. Чем я могу вам помочь?")
    elif (message.text == "Прямой"):
        active_sessions[message.chat.id] = 1
        hideBoard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton("В главное меню📱")
        hideBoard.add(btn3)
        bot.send_message(message.chat.id, text="Введите адрес отправления и прибытия в формате: Город отправления -> Город прибытия",
                         reply_markup=hideBoard)
    elif (message.text == "Экскурсионный"):
        active_sessions[message.chat.id] = 2
        hideBoard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn3 = types.KeyboardButton("В главное меню📱")
        hideBoard.add(btn3)
        bot.send_message(message.chat.id, text="Введите адрес отправления и прибытия в формате: Город отправления -> Город прибытия",
                         reply_markup=hideBoard, parse_mode='MARKDOWN')
    elif (message.text == "В главное меню📱"):
        active_sessions[message.chat.id] = 0
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Построить маршрут")
        btnGuide = types.KeyboardButton("Пообщаться с гидом")
        markup.add(btnGuide)
        markup.add(btn1)
        bot.send_message(message.chat.id,
                         text="Добро пожаловать в бот для построения маршрутов".format(
                             message.from_user), reply_markup=markup, parse_mode='MARKDOWN')
    elif active_sessions[message.chat.id] == 1:
        s = str(message.text)
        try:
            s2 = list(map(str, s.split("->")))
            link = gis.getLink(s2[1:], s2[0])
            bot.send_message(message.chat.id,
                             text=settings.makeLink(link), parse_mode="HTML")
            active_sessions[message.chat.id] = 0
        except Exception as e:
            logging.error(e)
            bot.send_message(message.chat.id,
                             text="Неправильный формат данных. Введите снова".format(
                                 message.from_user))
    elif active_sessions[message.chat.id] == 2:
        s = str(message.text)
        try:
            s2 = list(map(str, s.split("->")))
            attractions = []
            for i in range(1, len(s2)):
                answer = AIResponse(s2[i], GigaChat, GigaRet)
                attractions = attractions + gis.split(s2[i], answer)
            link = gis.getLink(attractions, s2[0])
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btnGuide = types.KeyboardButton("Пообщаться с гидом")
            markup.add(btnGuide)
            bot.send_message(message.chat.id,
                             text=settings.makeLink(link), parse_mode="HTML", reply_markup=markup)
            active_sessions[message.chat.id] = 0
            # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            # btnGuide = types.KeyboardButton("Узнать поподробнее об этих достопримечательностях")
            # markup.add(btnGuide)
            # bot.send_message(message.chat.id,
            #                  text="".format(
            #                      message.from_user), reply_markup=markup)
        except Exception as e:
            logging.error(e)
            bot.send_message(message.chat.id,
                             text="Неправильный формат данных. Введите снова".format(
                                 message.from_user))
    else:
        s = str(message.text)
        bot.send_message(message.chat.id,
                         text=GptAnswer(s).format(
                             message.from_user))


bot.polling(none_stop=True)