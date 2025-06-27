import io
import pandas as pd 
import re
import ipaddress
from aiogram import types
from bot.create_bot import dp, bot
from sql.engine import engine

db = engine
async def command_ip(message: types.Message) -> None:
    output = io.BytesIO()
    df3 = pd.DataFrame({'operator': [], 'iccid': [], 'msisdn': [], 'ip': [], 'apn': [], 'apnusername': [], 'password': []})
    string = message.text
    for ip in find_ips_ipaddress(string):    
        conn = db.connect() 
        sql_query = pd.read_sql("select * from simcards where ip = %(ip)s;", con=conn, params={'ip': ip})
        df = pd.DataFrame(sql_query, columns = ['operator', 'iccid', 'msisdn', 'ip', 'apn', 'apnusername', 'password'])
        conn.close()
        num_rows = df.shape[0]
        if num_rows > 0 :
            df3 = pd.concat([df3, df], ignore_index=True)
        else :
            df3.loc[len(df3.index)] = ['нет данных', 'нет данных', 'нет данных', ip, 'нет данных', 'нет данных', 'нет данных']
    num_rows = df3.shape[0] 
    if num_rows > 0 and num_rows < 2 :
        operator = df3['operator'].squeeze()
        iccid = df3['iccid'].squeeze() 
        msisdn = df3['msisdn'].squeeze()
        ip = df3['ip'].squeeze()
        apnname = df3['apn'].squeeze()
        apnusername = df3['apnusername'].squeeze()
        password = df3['password'].squeeze()
        await message.reply(
            f"<b>operator:</b> {operator}\n"
            f"<b>iccid:</b> {iccid}\n"
            f"<b>msisdn:</b> {msisdn}\n"
            f"<b>ip:</b> {ip}\n"
            f"<b>apname:</b> {apnname}\n"
            f"<b>apnusername:</b> {apnusername}\n"    
            f"<b>password:</b> {password}\n",
            parse_mode = 'HTML'                   
        )
    if num_rows > 1 :
        df3.to_excel(output, index=False)
        document = output.getvalue()
        await bot.send_document(message.chat.id, ('response.xlsx', document))
        output.close()

def find_ips_ipaddress(string):
    ips = []
    for ip1 in string.split(" "):
        try:
            ip = ipaddress.ip_address(ip1)
            ips.append(str(ip))
        except ValueError:
            pass
    return ips