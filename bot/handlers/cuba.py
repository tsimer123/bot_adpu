import pandas as pd
import xlsxwriter
import datetime
import requests
import json
import os
from io import BytesIO
from aiogram import types
from bot.create_bot import bot
from sql.engine import engine
from dotenv import load_dotenv

load_dotenv()

authorization = os.getenv('authorization')
username = os.getenv('username')
password = os.getenv('password')

db = engine
async def command_cuba(message: types.Message) -> None:
    url = 'http://192.1.0.226:8080/rest/v2/oauth/token'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded', 
        'Authorization': authorization
    }
    payload = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }
    with requests.Session() as session:
        session.post(url, headers=headers, data=payload)
        url = 'http://192.1.0.226:8080/rest/v2/entities/pnrservices_SM160LogInfo?view=sM160LogInfo-view'
        r = session.get(url)
    df = pd.DataFrame(r.json())
    df['smallVersionPo']=df['smallVersionPo'].astype(str)
    df['bigVersionPo'] = df['bigVersionPo'].astype(str)
    df['smallVersionPo']=df['smallVersionPo'].replace(to_replace='nan', value='ffff')
    df['bigVersionPo'] = df['bigVersionPo'].replace(to_replace='nan', value='00')
    df['bigVersionPo']= pd.to_numeric(df['bigVersionPo'], downcast='signed')
    df['smallVersionPo'] = df['smallVersionPo'].map(lambda x: int (x, 16))
    df['smallVersionPo'] = df['smallVersionPo'].astype(str)
    df['bigVersionPo'] = df['bigVersionPo'].astype(str)
    df['VersionPo'] = df['bigVersionPo'] + '.' + df['smallVersionPo']
    df['VersionPo'] = df['VersionPo'].replace(to_replace='0.65535', value='')
    df = df.drop(df.columns[[0, 1, 10, 11]], axis=1)
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