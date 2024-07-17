import io
import pandas as pd 
import re
from aiogram import types
from bot.create_bot import dp, bot
from sql.engine import engine

db = engine
async def command_imsi(message: types.Message) -> None:
    output = io.BytesIO()
    df3 = pd.DataFrame({'operator': [], 'iccid': [], 'msisdn': [], 'ip': [], 'apn': [], 'apnusername': [], 'password': []})
    string = message.text
    items = [
        m.group()
        for m in re.finditer(r"(89701)([0-9]{12,15})", string)
        ]
    for iccid1 in items:    
        conn = db.connect() 
        sql_query = pd.read_sql("select * from simcards where iccid = %(iccid)s;", con=conn, params={'iccid': iccid1})
        df = pd.DataFrame(sql_query, columns = ['operator', 'iccid', 'msisdn', 'ip', 'apn', 'apnusername', 'password'])
        conn.close()
        num_rows = df.shape[0]
        if num_rows > 0 :
            df3 = pd.concat([df3, df], ignore_index=True)
        else :
            df3.loc[len(df3.index)] = ['нет данных', iccid1, 'нет данных', 'нет данных', 'нет данных', 'нет данных', 'нет данных']
            # await message.reply(
            #     f"Информация отсутствует по\n"
            #     f"<b>iccid:</b> {iccid1}\n",
            #     parse_mode = 'HTML'
            # ) 
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