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

db = engine
async def command_emeter(message: types.Message) -> None:
    string = message.text
    string = string.split()
    conn = db.connect()
    sql_query = pd.read_sql("SELECT id, user_id, username, first_name, last_name, number_meter, imei, iccid1, iccid2, latitude, longitude, montag, power, created_on, state_meter FROM meter order by id;", con=conn)
    df = pd.DataFrame(sql_query, columns = ['id', 'user_id', 'username', 'first_name', 'last_name', 'number_meter', 'imei', 'iccid1', 'iccid2', 'latitude','longitude', 'montag', 'power', 'created_on', 'state_meter'])
    conn.close()
    filename = "meter {}.xlsx".format(datetime.date.today().strftime("%d.%m.%y"))
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Лист1')
        worksheet = writer.sheets['Лист1']
        worksheet.autofit()
        (max_row, max_col) = df.shape
        column_settings = [{'header': column} for column in df.columns]
        worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings, 'style': 'Table Style Medium 11' })
    msg['To'] = string[1]
    attach_file_to_email(msg, filename)
    send_mail_smtp(msg, host, login, password, filename)
    await message.reply("Проверьте почту")
    
load_dotenv()
login = os.getenv('login')
password = os.getenv('epassword')
host = "smtp.yandex.ru"

msg = EmailMessage()
msg['Subject'] = 'meter'
msg['From'] = login
msg.set_content('See attached file')

def attach_file_to_email(email, filename):
    with open(filename, 'rb') as fp:
        file_data = fp.read()
        maintype, _, subtype = (mimetypes.guess_type(filename)[0] or 'application/octet-stream').partition("/")
        email.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)

def send_mail_smtp(mail, host, username, password, filename):
    s = smtplib.SMTP(host)
    try:
        s.starttls()
        s.login(username, password)
        s.send_message(mail)       
    except Exception as ex:
        print(ex)
    finally:
        os.remove(filename)
        s.quit()