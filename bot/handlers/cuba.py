import pandas as pd
import xlsxwriter
import datetime
import requests
import json
from io import BytesIO
from aiogram import types
from bot.create_bot import bot
from sql.engine import engine

db = engine
async def command_cuba(message: types.Message) -> None:
    url = 'http://192.1.0.226:8080/rest/v2/oauth/token'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded', 
        'Authorization': 'Basic cG5yc2VydmljZXMtM1JHY1RGYWc6Yzg1YjhmYzQ4NzQ0OTFhMzkxZDhlZmJjMGNiM2Y4MWE1M2FkNTgwMDQ4YjcyZjRjZDQwMzVkODliYmRmNzU4Yw=='
    }
    payload = {
        'grant_type': 'password',
        'username': 'pnr',
        'password': 'Z{?c#H'
    }
    with requests.Session() as session:
        session.post(url, headers=headers, data=payload)
        url = 'http://192.1.0.226:8080/rest/v2/entities/pnrservices_SM160LogInfo'
        r = session.get(url)
    df = pd.DataFrame(r.json())
    filename = "output {}.xlsx".format(datetime.date.today().strftime("%d.%m.%y"))
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