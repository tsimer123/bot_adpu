from aiogram import types, Dispatcher

from bot.create_bot import dp, bot

from bot.handlers.start import command_start
from bot.handlers.help import command_help
from bot.handlers.coord import command_coord
from bot.handlers.sims import command_sims_tel_and_iccid

def register_handler_client(db: Dispatcher):
    #dp.register_message_handler(unknown_message, content_types=['ANY'])
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_coord, commands=['coord'])
    dp.register_message_handler(command_sims_tel_and_iccid, commands=['tel'])
    dp.register_message_handler(command_sims_tel_and_iccid, commands=['iccid'])

    