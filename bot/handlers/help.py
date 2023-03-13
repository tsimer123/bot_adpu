from aiogram import types
from datetime import datetime

async def command_help(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))

    list_help = []
    str_help = ''

    with open("help.html", 'r', encoding='utf8') as f_help:
        list_help = f_help.readlines()
    for line_f in list_help:
        str_help += line_f
    # await message.reply(str_help, parse_mode="MarkdownV2")
    await message.reply(str_help, parse_mode=types.ParseMode.HTML)
