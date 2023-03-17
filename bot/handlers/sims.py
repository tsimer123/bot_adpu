from aiogram import types
import re

from services.command_start import start_user
from services.log import write_log
from services.render_replay_str import print_format_log_cmd
from bot.handlers.str_description_err import error_1001, error_1003, error_not_sim_in_db, error_valid_number_tel,\
error_valid_iccid
from services.command_sims_num_iccid import input_data

async def command_sims_tel_and_iccid(message: types.Message) -> None:
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

        result = input_data(split_message(message_text))

        if result['sims_id'] != 0:
            str_for_replay = format_replay_str(result)
            log_id_db = write_log(users_id_db, 'output', str_for_replay)
            print_format_log_cmd(list_param_log_cmd, 'out', 'ok')
            await message.reply(str_for_replay)
        else:
            if result['description'] == "Error DB, no sims in table":
                print_format_log_cmd(list_param_log_cmd, 'out', 'code error: 1001')
                log_id_db = write_log(users_id_db, 'output', 'code error: 1001')
                await message.reply(error_1001)
            
            if result['description'] == "Not sim in DB":
                print_format_log_cmd(list_param_log_cmd, 'out', 'Not sim in DB')
                log_id_db = write_log(users_id_db, 'output', 'Not sim in DB')
                await message.reply(error_not_sim_in_db)
            
            if result['description'] == "Not valid number tel":
                print_format_log_cmd(list_param_log_cmd, 'out', 'Not valid number tel')
                log_id_db = write_log(users_id_db, 'output', 'Not valid number tel')
                await message.reply(error_valid_number_tel)

            if result['description'] == "Not valid iccid":
                print_format_log_cmd(list_param_log_cmd, 'out', 'Not valid iccid')
                log_id_db = write_log(users_id_db, 'output', 'Not valid iccid')
                await message.reply(error_valid_iccid)

    except Exception as ex:
        print_format_log_cmd(list_param_log_cmd, 'err', ex.args[0])        
        await message.reply(error_1003)


def split_message(message_text: str) -> str:

    split_message = re.split(r"\s", message_text)

    split_message[0] = split_message[0].replace('/', '')
        
    return split_message


def format_replay_str(result):

    replay_msg = f"\
На Ваш запрос найдена sim карта:\n\
№ телефона: {result['number_tel']}\n\
ICCID: {result['iccid']}\n\
АПН: {result['apn']}\n\
IP: {result['ip']}\n\
Статус: {result['state']}\n\
Оператор: {result['operator']}\n\
IMEI: {result['imei']}\n\
Данные актуальны на: {result['last_upload']}"

    return replay_msg
