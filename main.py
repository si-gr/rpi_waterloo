import RPi.GPIO as GPIO
import time

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

from requests import get
import tableParser


admin_id = 195707881

GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

while True:
    GPIO.output(16, GPIO.HIGH)
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(16, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    time.sleep(5)




updater = Updater(token='461718350:AAEwA95TSfk698kPsc26DcQL1hkveRdS33I')
dispatcher = updater.dispatcher
bot_obj = updater.bot


def start(bot, update):
    print(update.effective_user.id)

def show(bot, update):
    msg = "hallo test"
    if(update.message.chat.id == 195707881):
        bot.send_message(chat_id=update.message.chat_id, disable_web_page_preview=True, parse_mode="markdown", text=msg)

start_handler = CommandHandler('start', start)
show_handler = CommandHandler('show', show)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(show_handler)
updater.start_polling()
