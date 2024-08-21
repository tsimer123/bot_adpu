from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot.create_bot import dp, bot

from bot.handlers.start import command_start
from bot.handlers.help import command_help
from bot.handlers.coord import command_coord
from bot.handlers.sims import command_sims_tel_and_iccid
from bot.handlers.imsi import command_imsi
from bot.handlers.msisdn import command_msisdn
from bot.handlers.sim import command_sim
from bot.handlers.cuba import command_cuba
from bot.handlers.bar import command_bar
from bot.handlers.document import download_document
from bot.handlers.text import extract_data

def register_handler_client(db: Dispatcher):
    #dp.register_message_handler(unknown_message, content_types=['ANY'])
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_coord, commands=['coord'])
    dp.register_message_handler(command_sims_tel_and_iccid, commands=['tel'])
    dp.register_message_handler(command_sims_tel_and_iccid, commands=['iccid'])
    dp.register_message_handler(command_imsi, commands=['imsi'])
    dp.register_message_handler(command_msisdn, commands=['msisdn'])
    dp.register_message_handler(command_sim, commands=['sim'])
    dp.register_message_handler(command_cuba, commands=['cuba'])
    dp.register_message_handler(command_bar, commands=['meter'], state="*")
    dp.register_message_handler(download_document, content_types=types.ContentType.DOCUMENT)
    dp.register_message_handler(extract_data)