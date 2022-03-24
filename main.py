import RPi.GPIO as GPIO
import time
import subprocess
import logging
import threading

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import platform
import serial
import os

ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

if os.path.getsize("python.log") > 200000:
    os.remove("python.log")

# Enable logging
logging.basicConfig(filename='python.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

admin_id = 195707881

GPIO.setmode(GPIO.BOARD)

pump_array = [16, 18, 19, 21]

for p in pump_array:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, GPIO.HIGH)

updater = Updater(token=open("/home/pi/workspace/token", "r").read().splitlines()[0])
dispatcher = updater.dispatcher
bot_obj = updater.bot

def read_from_port():
    while True:
        try:
            line = str(ser.read(1024).decode('utf8', errors='ignore')).replace("\n", " ")
            if len(line) > 2:
                print(line)
                logger.info(line)
        except Exception as e:
            print(e)

thread = threading.Thread(target=read_from_port)
thread.start()

def start(bot, context):
    print(bot.effective_user.id)

def toggle(bot, context):
    if bot.effective_user.id == admin_id:
        if(len(context.args) == 0):
            return
        GPIO.output(pump_array[int(context.args[0])], GPIO.LOW)
        if(len(context.args) == 2):
            time.sleep(int(context.args[1]))
        else:
            time.sleep(5)
        GPIO.output(pump_array[int(context.args[0])], GPIO.HIGH)
        bot.message.reply_markdown_v2(
            "Pump run: " + str(pump_array[int(context.args[0])]))

# git pull
def reload(bot, context):
    process = subprocess.Popen("git pull".split(), cwd="/home/pi/workspace/rpi_waterloo", stdout=subprocess.PIPE)
    time.sleep(20)
    output, _ = process.communicate()
    bot.message.reply_text(str(output))

def get_flower(bot, context):
    read_file = open("/home/pi/workspace/rpi_waterloo/python.log", "r")
    print("flower command")
    res = []
    lines = read_file.readlines()
    for line in range(0, len(lines)):
        if "Real " in lines[line]:
            r = ""
            for l2 in lines[line - 8:line]:
                if "2022" in l2:
                    r += l2
            res += [r[:19] + " " + lines[line][13:]]
    bot.message.reply_text(res[-1])
    read_file.close()

def osinfo(update: Update, context: CallbackContext) -> None:
        update.message.reply_text("System: "+platform.uname()[0]+"\n"+"Node: "+platform.uname()[1]+"\n"+"Release: "+platform.uname()[2]+"\n"+"Version: "+platform.uname()[3]+"\n"+"Machine: "+platform.uname()[4]+"\n"+"Processor: "+platform.uname()[5])

def chunkstring(string,length):
    return (string[0 + i:length + i] for i in range(0, len(string), length))

def execute(update: Update, context:CallbackContext) -> None:
    print(update.message.text)
    user = update.message.from_user
    if user.id == admin_id:
        try:
            p = subprocess.run(update.message.text, shell=True, capture_output=True, timeout=5)
            out=p.stdout
            if int(len(out)) < 4090:
                update.message.reply_text(out.decode("latin-1"))
            else:
                for element in list(chunkstring(out,4090)):
                    print(element)
                    update.message.reply_text(element.decode("latin-1"))
        except subprocess.TimeoutExpired as err:
            update.message.reply_text("Timeout", parse_mode="html")
        except Exception as e:
            print(e)
            update.message.reply_text(f"<b>Command error.</b> {e}", parse_mode="html")
    else:
        update.message.reply_text("<b>Command error.</b>", parse_mode="html")

start_handler = CommandHandler('start', start)
show_handler = CommandHandler('toggle', toggle)
reload_handler = CommandHandler('reload', reload)
flower_handler = CommandHandler('flower', get_flower)
dispatcher.add_handler(CommandHandler("osinfo", osinfo))
dispatcher.add_handler(start_handler)
dispatcher.add_handler(show_handler)
dispatcher.add_handler(reload_handler)
dispatcher.add_handler(flower_handler)
# on non command i.e message - echo the message on Telegram
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, execute))
updater.start_polling()