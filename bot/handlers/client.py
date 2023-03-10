from aiogram import types, Dispatcher

from bot.create_bot import dp, bot

from bot.handlers.start import command_start
from bot.handlers.help import command_help
from bot.handlers.coord import command_coord

def register_handler_client(db: Dispatcher):
    #dp.register_message_handler(unknown_message, content_types=['ANY'])
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_coord, commands=['coord'])

    