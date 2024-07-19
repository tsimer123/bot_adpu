import io
import pandas as pd 
import re
from aiogram import types
from bot.create_bot import dp, bot
from sql.engine import engine
from sqlalchemy.types import Text

db = engine
async def download_document(message: types.Message) -> None:
    output = io.BytesIO()
    output2 = io.BytesIO()
    await message.document.download(destination = output)
    output.getvalue()
    df2 = pd.read_excel(output, dtype=object)
    if df2.columns[0] == 'msisdn':
        conn = db.connect()
        df2.to_sql('simki', con=conn, if_exists='replace', index=False) 
        sql_query = pd.read_sql("SELECT simcards.msisdn, simcards.iccid, simcards.operator, simcards.ip, simcards.apn, simcards.apnusername, simcards.password, simcards.issued, simcards.date_receipt FROM simcards, simki where simcards.msisdn=simki.msisdn;", con=conn)
        df = pd.DataFrame(sql_query, columns = ['msisdn', 'iccid', 'operator', 'ip', 'apn', 'apnusername', 'password'])
        conn.close()
        df2["msisdn"] = df2['msisdn'].astype('int')
        df["msisdn"] = df['msisdn'].astype('int')
        df2 = df2.merge(df, how='left', on='msisdn')
        df2 = df2.fillna('Нет данных')
        df2.to_excel(output2, index=False)
        document = output2.getvalue()
        await bot.send_document(message.chat.id, ('response.xlsx', document))
    elif df2.columns[0] == 'imsi':
        conn = db.connect()
        df2.to_sql('simki', con=conn, if_exists='replace', index=False) 
        sql_query = pd.read_sql("SELECT simcards.iccid, simcards.msisdn, simcards.operator, simcards.ip, simcards.apn, simcards.apnusername, simcards.password, simcards.issued, simcards.date_receipt FROM simcards, simki where simcards.iccid=simki.imsi;", con=conn)
        df = pd.DataFrame(sql_query, columns = ['iccid', 'msisdn', 'operator', 'ip', 'apn', 'apnusername', 'password'])
        conn.close()
        df2 = df2.rename(columns={'imsi': 'iccid'})
        df2["iccid"] = df2['iccid'].astype('int')
        df["iccid"] = df['iccid'].astype('int')
        df2 = df2.merge(df, how='left', on='iccid')
        df2 = df2.fillna('Нет данных')
        df2.to_excel(output2, index=False)
        document = output2.getvalue()
        await bot.send_document(message.chat.id, ('response.xlsx', document))
    elif df2.columns[0] == 'iccid':
        conn = db.connect()
        df2.to_sql('simki', con=conn, if_exists='replace', index=False) 
        sql_query = pd.read_sql("SELECT sims.iccid, sims.number_tel, sims.apn, sims.ip, sims.state, sims.activity, sims.traffic, sims.operator, sims.imei FROM sims, simki where sims.iccid=simki.iccid and sims.state_in_lk='present';", con=conn)
        df = pd.DataFrame(sql_query, columns = ['iccid', 'number_tel', 'apn', 'ip', 'state', 'activity', 'traffic', 'operator', 'imei'])
        conn.close()
        df2["iccid"] = df2['iccid'].astype('int')
        df["iccid"] = df['iccid'].astype('int')
        df2 = df2.merge(df, how='left', on='iccid')
        df2 = df2.fillna('Нет данных')
        df2.to_excel(output2, index=False)
        document = output2.getvalue()
        await bot.send_document(message.chat.id, ('response.xlsx', document))
    elif df2.columns[0] == 'tel':
        conn = db.connect()
        df2.to_sql('simki', con=conn, if_exists='replace', index=False, dtype={"tel": Text()}) 
        sql_query = pd.read_sql("SELECT sims.number_tel as tel, sims.iccid, sims.apn, sims.ip, sims.state, sims.activity, sims.traffic, sims.operator, sims.imei FROM sims, simki where sims.number_tel=simki.tel and sims.state_in_lk='present';", con=conn)
        df = pd.DataFrame(sql_query, columns = ['tel', 'iccid', 'apn', 'ip', 'state', 'activity', 'traffic', 'operator', 'imei'])
        conn.close()
        df2["tel"] = df2['tel'].astype('int')
        df["tel"] = df['tel'].astype('int')
        df2 = df2.merge(df, how='left', on='tel')
        df2 = df2.fillna('Нет данных')
        df2.to_excel(output2, index=False)
        document = output2.getvalue()
        await bot.send_document(message.chat.id, ('response.xlsx', document))
    else:
        await message.reply(
                    f"<b>Обрабатываются только файлы с названиями первых столбцов iccid, msisdn, tel или imsi</b>",
                    parse_mode = 'HTML'
        )
