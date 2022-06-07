import smtplib
import time

from config import SENDER_LOGIN, SENDER_PASSWORD, robot1, robot2
from robot_checker import is_free
from loader import bot
from handlers.messages.bot_message import lang_message


async def send_email(data, chat_id, lang):
    sender = SENDER_LOGIN
    password = SENDER_PASSWORD

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    try:
        sent = 0
        server.login(sender, password)
        while sent == 0:
            if is_free(robot1):
                server.sendmail(sender, robot1, data)
                sent = 1
                await bot.send_message(chat_id, lang_message.get(lang).get('data_sent'))
            elif is_free(robot2):
                server.sendmail(sender, robot2, data)
                sent = 1
                await bot.send_message(chat_id, lang_message.get(lang).get('data_sent'))
            else:
                await bot.send_message(chat_id, lang_message.get(lang).get('not_free'))
                time.sleep(300)

    except Exception as e:
        print(e)
