#!/usr/bin/python
#pip install gtts telebot

import re 
import gtts
import telebot
from config import *


def telegram_bot(API_TOKEN):
    bot = telebot.TeleBot(API_TOKEN)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.send_message(message.chat.id, WELCOME_MESSAGE)

    @bot.message_handler(content_types=['text'])
    def text_to_speech(message):
        #The simplest language detection. Works with 'ru' and 'en'.
        detected_lang = 'ru' if re.search('[А-яЁё]', message.text) else 'en'

        if DEBUG_MODE:
            bot.send_message(message.chat.id, 
                             DEBUG_MESSAGE.format(message.text, detected_lang))

        tss = gtts.gTTS(message.text, lang=detected_lang)
        tss.save('converted_text.mp3')

        bot.send_audio(message.chat.id, open('converted_text.mp3', 'rb'))

    bot.polling()


if __name__ == '__main__':
    telegram_bot(API_TOKEN)
