import RPi.GPIO as GPIO
import time
import subprocess

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters


admin_id = 195707881

GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

pump_array = [16, 18, 19, 21]

updater = Updater(token=open("/home/pi/workspace/token", "r").read().splitlines()[0])
dispatcher = updater.dispatcher
bot_obj = updater.bot


def start(bot, context):
    print(bot.effective_user.id)

def toggle(bot, context):
    if bot.effective_user.id == admin_id:
        if(len(context.args) == 0):
            return
        GPIO.output(pump_array[int(context.args[0])], GPIO.HIGH)
        time.sleep(2)
        GPIO.output(pump_array[int(context.args[0])], GPIO.LOW)
        bot.message.reply_markdown_v2(
            "Pump run: " + str(pump_array[int(context.args[0])]))

# git pull
def reload(bot, context):
    process = subprocess.Popen("git pull", cwd="/home/pi/workspace/rpi_waterloo", stdout=subprocess.PIPE)
    time.sleep(20)
    output, _ = process.communicate()
    bot.message.reply_markdown_v2(output)

start_handler = CommandHandler('start', start)
show_handler = CommandHandler('toggle', toggle)
reload_handler = CommandHandler('reload', reload)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(show_handler)
dispatcher.add_handler(reload_handler)
updater.start_polling()