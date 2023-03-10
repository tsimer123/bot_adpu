from aiogram import types
from datetime import datetime

from bot.create_bot import bot
from services.command_start import start_user
from services.log import write_log

async def command_start(message: types.Message):
    try:
        id_user_tg = message.from_user.id
        full_name = message.from_user.full_name
        tg_name = message.from_user.mention
        
        users_id_db = start_user(id_user_tg, tg_name, full_name)      

        log_id_db = write_log(users_id_db, 'input', '/start')
        
        print(str(datetime.now()) + ", " +
              str(users_id_db) + ", " +
              "in " +
              str(log_id_db) + ", " +
              str(id_user_tg) + ", " +
              str(tg_name) + ", " +
              str(full_name) + ", " +
              '/start')
        await bot.send_message(message.from_user.id, 'Добро пожаловать' + " " + str(full_name))
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/SEK_ADPU_bot')