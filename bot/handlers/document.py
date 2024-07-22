import io
import pandas as pd
import re
import xlsxwriter
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
        df2.to_sql('simki', con=conn, if_exists='replace') 
        sql_query = pd.read_sql("SELECT msisdn, COALESCE(iccid, 'Нет данных') as iccid, COALESCE(operator, 'Нет данных') as operator, COALESCE(ip, 'Нет данных') as ip, COALESCE(apn, 'Нет данных') as apn, COALESCE(apnusername, 'Нет данных') as apnusername, COALESCE(password, 'Нет данных') as password FROM simki LEFT JOIN simcards USING (msisdn) order by simki.index;", con=conn)
        df = pd.DataFrame(sql_query, columns = ['msisdn', 'iccid', 'operator', 'ip', 'apn', 'apnusername', 'password'])
        conn.close()
        writer = pd.ExcelWriter(output2, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Лист1')
        workbook = writer.book
        worksheet = writer.sheets['Лист1']
        worksheet.autofit()
        workbook.close()
        document = output2.getvalue()
        await bot.send_document(message.chat.id, ('response.xlsx', document))
    elif df2.columns[0] == 'imsi':
        df2 = df2.rename(columns={'imsi': 'iccid'})
        conn = db.connect()
        df2.to_sql('simki', con=conn, if_exists='replace') 
        sql_query = pd.read_sql("SELECT iccid, COALESCE(msisdn, 'Нет данных') as msisdn, COALESCE(operator, 'Нет данных') as operator, COALESCE(ip, 'Нет данных') as ip, COALESCE(apn, 'Нет данных') as apn, COALESCE(apnusername, 'Нет данных') as apnusername, COALESCE(password, 'Нет данных') as password FROM simki LEFT JOIN simcards USING (iccid) order by simki.index;", con=conn)
        df = pd.DataFrame(sql_query, columns = ['iccid', 'msisdn', 'operator', 'ip', 'apn', 'apnusername', 'password'])
        conn.close()
        writer = pd.ExcelWriter(output2, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Лист1')
        workbook = writer.book
        worksheet = writer.sheets['Лист1']
        worksheet.autofit()
        workbook.close()
        document = output2.getvalue()
        await bot.send_document(message.chat.id, ('response.xlsx', document))
    elif df2.columns[0] == 'iccid':
        conn = db.connect()
        df2.to_sql('simki', con=conn, if_exists='replace') 
        sql_query = pd.read_sql("SELECT iccid, COALESCE(number_tel, 'Нет данных') as tel, COALESCE(apn, 'Нет данных') as apn, COALESCE(ip, 'Нет данных') as ip, COALESCE(state, 'Нет данных') as state, activity, COALESCE(traffic, 'Нет данных') as traffic, COALESCE(operator, 'Нет данных'), COALESCE(imei, 'Нет данных') as imei FROM simki LEFT JOIN sims USING (iccid) where sims.state_in_lk='present' order by simki.index;", con=conn)
        df = pd.DataFrame(sql_query, columns = ['iccid', 'number_tel', 'apn', 'ip', 'state', 'activity', 'traffic', 'operator', 'imei'])
        conn.close()
        writer = pd.ExcelWriter(output2, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Лист1')
        workbook = writer.book
        worksheet = writer.sheets['Лист1']
        worksheet.autofit()
        workbook.close()
        document = output2.getvalue()
        await bot.send_document(message.chat.id, ('response.xlsx', document))
    elif df2.columns[0] == 'tel':
        df2 = df2.rename(columns={'tel': 'number_tel'})
        conn = db.connect()
        df2.to_sql('simki', con=conn, if_exists='replace', dtype={"number_tel": Text()}) 
        sql_query = pd.read_sql("SELECT number_tel as tel, COALESCE(iccid, 'Нет данных') as iccid, COALESCE(apn, 'Нет данных') as apn, COALESCE(ip, 'Нет данных') as ip, COALESCE(state, 'Нет данных') as state, activity, COALESCE(traffic, 'Нет данных') as traffic, COALESCE(operator, 'Нет данных'), COALESCE(imei, 'Нет данных') as imei FROM simki LEFT JOIN sims USING (number_tel) where sims.state_in_lk='present' order by simki.index;", con=conn)
        df = pd.DataFrame(sql_query, columns = ['tel', 'iccid', 'apn', 'ip', 'state', 'activity', 'traffic', 'operator', 'imei'])
        conn.close()
        writer = pd.ExcelWriter(output2, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Лист1')
        workbook = writer.book
        worksheet = writer.sheets['Лист1']
        worksheet.autofit()
        workbook.close()
        document = output2.getvalue()
        await bot.send_document(message.chat.id, ('response.xlsx', document))
    elif df2.columns[0] == 'ip':
        conn = db.connect()
        df2.to_sql('simki', con=conn, if_exists='replace') 
        sql_query = pd.read_sql("SELECT ip, COALESCE(msisdn, 'Нет данных') as msisdn, COALESCE(iccid, 'Нет данных') as iccid, COALESCE(operator, 'Нет данных') as operator, COALESCE(apn, 'Нет данных') as apn, COALESCE(apnusername, 'Нет данных') as apnusername, COALESCE(password, 'Нет данных') as password FROM simki LEFT JOIN simcards USING (ip) order by simki.index;", con=conn)
        df = pd.DataFrame(sql_query, columns = ['ip', 'msisdn', 'iccid', 'operator', 'apn', 'apnusername', 'password'])
        conn.close()
        writer = pd.ExcelWriter(output2, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Лист1')
        workbook = writer.book
        worksheet = writer.sheets['Лист1']
        worksheet.autofit()
        workbook.close()
        document = output2.getvalue()
        await bot.send_document(message.chat.id, ('response.xlsx', document))
    else:
        await message.reply(
                    f"<b>Обрабатываются только файлы с названиями первых столбцов ip, iccid, msisdn, tel или imsi</b>",
                    parse_mode = 'HTML'
        )