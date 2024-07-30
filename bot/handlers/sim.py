import pandas as pd
import xlsxwriter
import datetime
from io import BytesIO
from aiogram import types
from bot.create_bot import bot
from sql.engine import engine

db = engine
async def command_sim(message: types.Message) -> None:
    conn = db.connect()
    sql_query = pd.read_sql("SELECT sims_id, number_tel, iccid, apn, ip, state, activity, traffic, operator, imei, state_in_lk, last_upload, created_on, update_on, hash_data FROM sims where sims.state_in_lk='present' order by sims_id;", con=conn)
    df = pd.DataFrame(sql_query, columns = ['sims_id', 'number_tel', 'iccid', 'apn', 'ip', 'state', 'activity', 'traffic', 'operator', 'imei', 'state_in_lk', 'last_upload', 'created_on', 'update_on', 'hash_data'])
    conn.close()
    filename = "Все сим карты {}.xlsx".format(datetime.date.today().strftime("%d.%m.%y"))
    await bot.send_document(message.chat.id, (filename, fit(df)))

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