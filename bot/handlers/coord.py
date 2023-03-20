from aiogram import types
from datetime import datetime
import re

from services.command_start import start_user
from services.log import write_log
from services.command_cord import serch_uspd
from services.render_replay_str import print_format_log_cmd
from bot.handlers.str_description_err import error_1001, error_1002,\
    error_not_valid_coord, error_1003, error_500m, error_valid_comand_coord
from bot.handlers.check_commands import check_len_command

async def command_coord(message: types.Message):
    id_user_tg = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    message_text = str(message.text)

    list_param_log_cmd = [0, 0, id_user_tg, tg_name, full_name]

    try:    
        users_id_db = start_user(id_user_tg, tg_name, full_name)

        log_id_db = write_log(users_id_db, 'input', message_text)

        list_param_log_cmd[0] = users_id_db
        list_param_log_cmd[1] = log_id_db        
            
        print_format_log_cmd(list_param_log_cmd, 'in', message_text)

        if check_len_command(message_text):
        
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
                    log_id_db = write_log(users_id_db, 'output', 'code error: 1001')
                    await message.reply(error_1001)
                
                if result['descriprion'] == "Error DB, not valid uquipment":
                    print_format_log_cmd(list_param_log_cmd, 'out', 'code error: 1002')
                    log_id_db = write_log(users_id_db, 'output', 'code error: 1002')
                    await message.reply(error_1002)
                
                if result['descriprion'] == "No valid source coordinates":
                    print_format_log_cmd(list_param_log_cmd, 'out', 'No valid source coordinates')
                    log_id_db = write_log(users_id_db, 'output', 'No valid source coordinates')
                    await message.reply(error_not_valid_coord)

                if result['descriprion'] == "Dist more than 500 m, no ZB network connection":
                    print_format_log_cmd(list_param_log_cmd, 'out', 'Dist more than 500 m')
                    log_id_db = write_log(users_id_db, 'output', 'Dist more than 500 m')
                    await message.reply(error_500m)
        else:
            print_format_log_cmd(list_param_log_cmd, 'out', 'Not valid command coord')
            log_id_db = write_log(users_id_db, 'output', 'Not valid command coord')
            await message.reply(error_valid_comand_coord)
    except Exception as ex:
        print_format_log_cmd(list_param_log_cmd, 'err', ex.args[0])        
        await message.reply(error_1003)



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
