import telebot

from config import settings, stickers

from body_functions import help_bot
from body_functions import add_alert_bot, alert_bot
from body_functions import ip_bot, ban_bot, unban_bot

from db_operations import get_legal_users


bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)


@bot.message_handler(func = lambda message: message.chat.id not in get_legal_users())
def unknown_bot_user(message):
   bot.send_message(message.chat.id, "are u czi guy?..")
   

@bot.message_handler(commands=['start'])
def start_bot_command(message):
    bot.send_photo(message.chat.id, photo=open(r'images/start-hello.jpg', 'rb'))


@bot.message_handler(commands=['help'])
def help_bot_command(message):
    response = help_bot()
    bot.reply_to(message, response, parse_mode="markdown")


@bot.message_handler(commands=['ban'])
def ban_bot_command(message):
    response = ban_bot(message.text, message.from_user.username)
    bot.reply_to(message, response, parse_mode="markdown")


@bot.message_handler(commands=['unban'])
def unban_bot_command(message):
    response = unban_bot(message.text)
    bot.reply_to(message, response, parse_mode="markdown")


@bot.message_handler(commands=['ip'])
def ip_bot_command(message):
    response = ip_bot(message.text)
    bot.reply_to(message, response, parse_mode="markdown")


@bot.message_handler(commands=['alert'])
def alert_bot_command(message):
    response = alert_bot(message.text)
    bot.reply_to(message, response, parse_mode="markdown")


@bot.message_handler(commands=['addalert'])
def add_alert_bot_command(message):
    response = add_alert_bot(message.text, message.from_user.username)
    bot.reply_to(message, response, parse_mode="markdown")


@bot.message_handler()
def get_ip_by_date(message):
    bot.send_sticker(message.chat.id, stickers.STICKER_EPIC_SAD)


bot.infinity_polling()
