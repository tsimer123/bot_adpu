import io
import pandas as pd 
import re
from aiogram import types
from bot.create_bot import dp, bot
from sql.engine import engine

db = engine
async def download_document(message: types.Message) -> None:
    output = io.BytesIO()
    output2 = io.BytesIO()
    await message.document.download(destination = output)
    df3 = pd.DataFrame({'operator': [], 'iccid': [], 'msisdn': [], 'ip': [], 'apn': [], 'apnusername': [], 'password': []})
    output.getvalue()
    df2 = pd.read_excel(output)
    if df2.columns[0] == 'msisdn':
        for msisdn1 in df2['msisdn'].squeeze():
            msisdn1 = str(msisdn1)
            conn = db.connect()
            sql_query = pd.read_sql("select * from simcards where msisdn = %(msisdn)s;", con=conn, params={'msisdn': msisdn1})
            df = pd.DataFrame(sql_query, columns = ['operator', 'iccid', 'msisdn', 'ip', 'apn', 'apnusername', 'password'])
            df3 = pd.concat([df3, df], ignore_index=True)
            conn.close()
        df3.to_excel(output2, index=False)
        document = output2.getvalue()
        await bot.send_document(message.chat.id, ('response.xlsx', document))
    elif df2.columns[0] == 'iccid':
        for iccid1 in df2['iccid'].squeeze():
            iccid1 = str(iccid1)
            conn = db.connect()
            sql_query = pd.read_sql("select * from simcards where iccid = %(iccid)s;", con=conn, params={'iccid': iccid1})
            df = pd.DataFrame(sql_query, columns = ['operator', 'iccid', 'msisdn', 'ip', 'apn', 'apnusername', 'password'])
            df3 = pd.concat([df3, df], ignore_index=True)
            conn.close()
        df3.to_excel(output2, index=False)
        document = output2.getvalue()
        await bot.send_document(message.chat.id, ('response.xlsx', document))
    else:
        await message.reply(
                    f"<b>Обрабатываются только файлы с названиями первых столбцов iccid или msisdn</b>",
                    parse_mode = 'HTML'
        )
