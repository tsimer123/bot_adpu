import io
import pandas as pd 
import re
from aiogram import types
from bot.create_bot import dp, bot
from sql.engine import engine

db = engine
async def extract_data(message: types.Message) -> None:
    data = {
        "phone_number": "<N/A>"
    }
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            data[item.type] = item.get_text (message.text)
            conn = db.connect() 
            msisdn1 = data[item.type]
            if len(msisdn1) == 10 :
                 msisdn1 = msisdn1[:0] + '7' + msisdn1[0:]
            else :
                msisdn1 = msisdn1[1:]
            sql_query = pd.read_sql("select * from simcards where msisdn = %(msisdn)s;", con=conn, params={'msisdn': msisdn1})
            df = pd.DataFrame(sql_query, columns = ['operator', 'iccid', 'msisdn', 'ip', 'apn', 'apnusername', 'password'])
            operator = df['operator'].squeeze()
            iccid = df['iccid'].squeeze() 
            msisdn = df['msisdn'].squeeze()
            ip = df['ip'].squeeze()
            apnname = df['apn'].squeeze()
            apnusername = df['apnusername'].squeeze()
            password = df['password'].squeeze()
            conn.close()
            num_rows = df.shape[0]
            if num_rows > 0 :
                await message.reply(
                    f"<b>Phone:</b> {(data['phone_number'])}\n"
                    f"<b>operator:</b> {operator}\n"
                    f"<b>iccid:</b> {iccid}\n"
                    f"<b>msisdn:</b> {msisdn}\n"
                    f"<b>ip:</b> {ip}\n"
                    f"<b>apnname:</b> {apnname}\n"
                    f"<b>apnusername:</b> {apnusername}\n"    
                    f"<b>password:</b> {password}\n",
                    parse_mode = 'HTML'                  
                    )
            else :
                await message.reply(
                    f"Информация отсутствует по {data['phone_number']}\n",
                    parse_mode = 'HTML'
                    )  

