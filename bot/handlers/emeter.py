import os
import smtplib
import mimetypes
from email.message import EmailMessage
from dotenv import load_dotenv
import pandas as pd
import xlsxwriter
import datetime
from aiogram import types
from sql.engine import engine
import logging
from services.command_start import start_user
from services.log import write_log
from services.render_replay_str import print_format_log_cmd

db = engine
load_dotenv()
login = os.getenv('login')
password = os.getenv('epassword')
host = "smtp.yandex.ru"
async def command_emeter(message: types.Message) -> None:
    message_text = str(message.text)
    list_param_log_cmd = [0, 0, message.from_user.id, message.from_user.mention, message.from_user.full_name]
    try:
        list_param_log_cmd[0] = start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name)
        list_param_log_cmd[1] = write_log(start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name), 'input', message_text)
        print_format_log_cmd(list_param_log_cmd, 'in', message_text)
    except Exception as ex:
        print_format_log_cmd(list_param_log_cmd, 'err', ex.args[0])
        await message.reply('Ошибка Базы Данных (code error: 1003).\n Обратитесь к Администратору @etsimerman')
    string = message.text
    string = string.split()
    msg = EmailMessage()
    msg['Subject'] = 'meter'
    msg['From'] = login
    msg.set_content('See attached file')
    msg['To'] = string[1]
    try:
        conn = db.connect()
        sql_query = pd.read_sql("SELECT id, user_id, username, first_name, last_name, number_meter, imei, iccid1, iccid2, latitude, longitude, number_task, montag, power, created_on, state_meter FROM meter order by id;", con=conn)
        df = pd.DataFrame(sql_query, columns = ['id', 'user_id', 'username', 'first_name', 'last_name', 'number_meter', 'imei', 'iccid1', 'iccid2', 'latitude','longitude', 'number_task', 'montag', 'power', 'created_on', 'state_meter'])   
    except Exception as ex:
        print_format_log_cmd(list_param_log_cmd, 'err', ex.args[0])
        return await message.reply("Сервис временно не доступен. Ошибка базы.")
    finally:
        conn.close()
    filename = "meter {}.xlsx".format(datetime.date.today().strftime("%d.%m.%y"))
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Лист1')
        worksheet = writer.sheets['Лист1']
        worksheet.autofit()
        (max_row, max_col) = df.shape
        column_settings = [{'header': column} for column in df.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings, 'style': 'Table Style Medium 11' })
    attach_file_to_email(msg, filename)
    messageerr = "Проверьте почту"
    send_mail_smtp(msg, host, login, password, filename, messageerr, message)
    await message.reply(messageerr)
    
def attach_file_to_email(email, filename):
    with open(filename, 'rb') as fp:
        file_data = fp.read()
        maintype, _, subtype = (mimetypes.guess_type(filename)[0] or 'application/octet-stream').partition("/")
        email.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)

def send_mail_smtp(mail, host, username, password, filename, messageerr, message):
    s = smtplib.SMTP(host)
    try:
        s.starttls()
        s.login(username, password)
        s.send_message(mail)       
    except Exception as ex:
        message_text = str(message.text)
        list_param_log_cmd = [0, 0, message.from_user.id, message.from_user.mention, message.from_user.full_name]
        list_param_log_cmd[0] = start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name)
        list_param_log_cmd[1] = write_log(start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name), 'input', message_text)
        print_format_log_cmd(list_param_log_cmd, 'err', ex.args[0])
        messageerr = ("Сервис временно не доступен. Ошибка почты.")
        return messageerr
    finally:
        os.remove(filename)
        s.quit()