from aiogram import types
from datetime import datetime
import re

from services.command_start import start_user
from services.log import write_log
from services.command_cord import serch_uspd

async def command_coord(message: types.Message):
    id_user_tg = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    message_text = str(message.text)
    
    users_id_db = start_user(id_user_tg, tg_name, full_name)

    log_id_db = write_log(users_id_db, 'input', message_text)

    list_param_log_cmd = [users_id_db, log_id_db, id_user_tg, tg_name, full_name]
        
    print_format_log_cmd(list_param_log_cmd, 'in', message_text)
    
    coord_from_msg = split_message(message_text)
    result = serch_uspd(coord_from_msg)

    if result['status']:
        str_for_replay = format_replay_str(result)
        log_id_db = write_log(users_id_db, 'output', str_for_replay)
        print_format_log_cmd(list_param_log_cmd, 'out', 'ok')
        await message.reply(str_for_replay)
    else:
        if result['descriprion'] == "Error DB, no equipment in table":
            print_format_log_cmd(list_param_log_cmd, 'out', 'code error: 1001')
            await message.reply('Ошибка Базы Данных (code error: 1001).\nОбратитесь к Администратору @etsimerman')
        
        if result['descriprion'] == "Error DB, not valid uquipment":
            print_format_log_cmd(list_param_log_cmd, 'out', 'code error: 1002')
            await message.reply('Ошибка Базы Данных (code error: 1002).\nОбратитесь к Администратору @etsimerman')
        
        if result['descriprion'] == "No valid source coordinates":
            print_format_log_cmd(list_param_log_cmd, 'out', 'No valid source coordinates')
            await message.reply('Координаты введены не верно.\nВерный формат:\n55.706792, 37.625540')        
        
        log_id_db = write_log(users_id_db, 'output', result['descriprion'])


def split_message(message_text):

    split_message = re.split(r"[;,\s]\s*", message_text)

    dict_coords = {
                "latitude": split_message[1],
                "longitude": split_message[2]
            }
    
    return dict_coords


def format_replay_str(result):

    replay_msg = f"\
На Ваш запрос найдено:\n\
Ближайшее оборудование: № {result['number_equipment']}\n\
Тип: {result['type_equipment']}\n\
Модель: {result['model_equipment']}\n\
Расстояние: {result['dist']}\n\
Широта: {result['latitude']}\n\
Долгота: {result['longitude']}\n\
№ телефона: {result['number_sim']}\n\
ICCID: {result['iccid']}\n\
Оператор: {result['operator']}\n\
Режим рабыты модема: {result['type_mode_modem']}\n"

    return replay_msg


def print_format_log_cmd(list_param, type, message):
    
    print(str(datetime.now()) + ", " +
            str(list_param[0]) + ", " +
            type + " " +
            str(list_param[1]) + ", " +
            str(list_param[2]) + ", " +
            str(list_param[3]) + ", " +
            str(list_param[4]) + ", " +
            str(message))
    