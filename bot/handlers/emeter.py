import os
import smtplib
import pandas as pd
import xlsxwriter
import datetime
from email.message import EmailMessage
from dotenv import load_dotenv
from aiogram import types
from sql.engine import engine
from services.command_start import start_user
from services.log import write_log
from services.render_replay_str import print_format_log_cmd
from io import BytesIO

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
    string = (message.text).split()
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
    msg.add_attachment(fit(df), maintype='application', subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=filename)
    await message.reply(send_mail_smtp(msg, host, login, password, message))

def send_mail_smtp(mail, host, username, password, message):
    try:
        s = smtplib.SMTP(host)
        s.starttls()
        s.login(username, password)
        s.send_message(mail)
        s.quit()
        text = "Проверьте почту"      
    except Exception as ex:
        list_param_log_cmd = [0, 0, message.from_user.id, message.from_user.mention, message.from_user.full_name]
        list_param_log_cmd[0] = start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name)
        list_param_log_cmd[1] = write_log(start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name), 'err', ex.args[0])
        print_format_log_cmd(list_param_log_cmd, 'err', ex.args[0])
        text = "Сервис временно не доступен. Ошибка почты."
    finally:
        return text

def fit (df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Лист1')
    workbook = writer.book
    worksheet = writer.sheets['Лист1']
    worksheet.autofit()
    (max_row, max_col) = df.shape
    column_settings = [{'header': column} for column in df.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings, 'style': 'Table Style Medium 11' })
    workbook.close()
    document = output.getvalue()
    return document