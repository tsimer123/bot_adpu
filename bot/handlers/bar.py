import logging
import aiogram.utils.markdown as md
import re
import asyncio
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from pyzbar import pyzbar
import cv2
from io import BytesIO, StringIO
from aiogram import types
from exif import Image
import datetime
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from bot.create_bot import dp, bot
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import insert
from sql.engine import engine
from sql.scheme import Meter
from sqlalchemy import text
from sqlalchemy.types import Text
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, BigInteger, Boolean
import time
from services.command_start import start_user
from services.log import write_log
from services.render_replay_str import print_format_log_cmd

class Form(StatesGroup):
    number_meter = State()
    imei = State()
    iccid1 = State()
    iccid2 = State()
    geo = State()
    number_task = State()
    montag = State()
    power = State()
    end = State()

@dp.message_handler(commands='meter')
async def command_bar(message: types.Message, state: FSMContext):
    message_text = str(message.text)
    list_param_log_cmd = [0, 0, message.from_user.id, message.from_user.mention, message.from_user.full_name]
    try:
        list_param_log_cmd[0] = start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name)
        list_param_log_cmd[1] = write_log(start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name), 'input', message_text)
        print_format_log_cmd(list_param_log_cmd, 'in', message_text)
    except Exception as ex:
        print_format_log_cmd(list_param_log_cmd, 'err', ex.args[0])
        await message.reply('Ошибка Базы Данных (code error: 1003).\n Обратитесь к Администратору @etsimerman')
    await Form.number_meter.set()
    await message.reply("Введите номер ПУ:\n Варианты ввода: \n - Пришлите фото с изображением штрихкода или QR-кода номера ПУ (используйте сжатие изображения при посылке, не присылайте сразу несколько штрихкодов на одном фото.)\n - Ввод номера ПУ вручную\n - Для прекращения ввода данных отправьте команду /cancel или слово - отмена")
    await asyncio.sleep(3600)
    current_state = await state.get_state()
    if current_state is None:
        return
    message_text = "таймаут"
    list_param_log_cmd = [0, 0, message.from_user.id, message.from_user.mention, message.from_user.full_name]
    list_param_log_cmd[0] = start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name)
    list_param_log_cmd[1] = write_log(start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name), 'input', message_text)
    textout = """Отменено по таймауту на состояние {current_st}"""
    textout = textout.format(current_st=current_state)
    print_format_log_cmd(list_param_log_cmd, 'in', textout)
    await state.finish()
    await message.reply('Отменено по таймауту', reply_markup=types.ReplyKeyboardRemove())
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(lambda msg: msg.text.lower() == 'отмена', state="*")
async def command_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    message_text = str(message.text)
    list_param_log_cmd = [0, 0, message.from_user.id, message.from_user.mention, message.from_user.full_name]
    list_param_log_cmd[0] = start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name)
    list_param_log_cmd[1] = write_log(start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name), 'input', message_text)
    textout = """Отменено на состояние {current_st}"""
    textout = textout.format(current_st=current_state)
    print_format_log_cmd(list_param_log_cmd, 'in', textout)
    await state.finish()
    await message.reply('Отменено', reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=Form.number_meter)    
@dp.message_handler(content_types=['photo', 'text'], state=Form.number_meter)
async def get_photo_text(message: types.Message, state: FSMContext):   
    if message.content_type == 'photo':
        await message.photo[-1].download('test.jpg')
        img = cv2.imread('test.jpg')
        decoded_objects = pyzbar.decode(img)
        if decoded_objects:
            for obj in decoded_objects:
                string = obj.data.decode()
                string = string.replace('-', '')
                if (string.isdigit() and len(string)>5):
                    async with state.proxy() as data:
                        if doublet('number_meter', string):
                            data['number_meter'] = string
                        else:
                            return await message.reply((f"Номер ПУ {string} не уникален.\nВведите номер ПУ (цифры только)"))   
                else:
                    return await message.reply(("Длина номера ПУ должна быть больше 5 цифр.\nВведите номер ПУ (цифры только)"))
        else:
            return await message.reply("Введите номер ПУ")
    elif message.content_type == 'text':     
        if (message.text.isdigit() and len(message.text)>5):
            async with state.proxy() as data:
                if doublet('number_meter', message.text):
                    data['number_meter'] = message.text
                else:
                    return await message.reply((f"Номер ПУ {message.text} не уникален.\nВведите номер ПУ (цифры только)"))
        else:
            return await message.reply(("Длина номера ПУ должна быть больше 5 цифр.\nВведите номер ПУ (цифры только)"))
    await Form.next()
    await message.reply("Введите IMEI:\n Варианты ввода: \n - Пришлите фото с изображением штрихкода или QR-кода IMEI (используйте сжатие изображения при посылке, не присылайте сразу несколько штрихкодов на одном фото.)\n - Ввод IMEI вручную")
    
@dp.message_handler(content_types=['photo', 'text'], state=Form.imei)
async def get_photo_text(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        await message.photo[-1].download('test.jpg')
        img = cv2.imread('test.jpg')
        decoded_objects = pyzbar.decode(img)
        if decoded_objects:
            for obj in decoded_objects:
                string = obj.data.decode()
                string = string.replace('-', '')
                if (string.isdigit() and len(string)>13 and len(string)<17):
                    async with state.proxy() as data:
                        if doublet('imei', string):
                            data['imei'] = string
                        else:
                            return await message.reply((f"IMEI {string} не уникален.\nВведите IMEI (цифры только)"))
                else:
                    return await message.reply(("Длина IMEI должна быть 14-16 цифр.\nВведите IMEI (цифры только)")) 
        else:
            return await message.reply("Введите IMEI")
    elif message.content_type == 'text':     
        if (message.text.isdigit() and len(message.text)>13 and len(message.text)<17):
            async with state.proxy() as data:
                if doublet('imei', message.text):
                    data['imei'] = message.text
                else:
                    return await message.reply((f"IMEI {message.text} не уникален.\nВведите IMEI (цифры только)"))
        else:
            return await message.reply(("Длина IMEI должна быть 14-16 цифр.\nВведите IMEI (цифры только)"))
    await Form.next()
    await message.reply("Введите ICCID1:\n Варианты ввода: \n - Пришлите фото с изображением штрихкода или QR-кода ICCID1 (используйте сжатие изображения при посылке, не присылайте сразу несколько штрихкодов на одном фото)\n - Ввод ICCID1 вручную")

@dp.message_handler(content_types=['photo', 'text'], state=Form.iccid1)
async def get_photo_text(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        await message.photo[-1].download('test.jpg')
        img = cv2.imread('test.jpg')
        decoded_objects = pyzbar.decode(img)
        if decoded_objects:
            for obj in decoded_objects:
                string = obj.data.decode()
                string = string.replace('-', '')
                if string.find('8970102') > 0 : string = string.slice(0, -1)  
                items = [
                iccid.group()
                for iccid in re.finditer(r"(89701)([0-9]{12,15})", string)
                ]
                if (string in items):
                    async with state.proxy() as data:
                        if doublet('iccid', string):
                            data['iccid1'] = string
                        else:
                            return await message.reply((f"ICCID1 {string} не уникален.\nВведите ICCID1 (цифры только)"))
                else:
                    return await message.reply(("Длина ICCID1 должна быть из 17-19 цифр начинающихся на 89701.\nВведите ICCID1 (цифры только)"))
        else:
            return await message.reply("Введите ICCID1")
    elif message.content_type == 'text':
        items = [
        iccid.group()
        for iccid in re.finditer(r"(89701)([0-9]{12,15})", message.text)
        ]
        if (message.text in items):
            async with state.proxy() as data:
                if doublet('iccid', message.text):
                    data['iccid1'] = message.text
                else:
                    return await message.reply((f"ICCID1 {message.text} не уникален.\nВведите ICCID1 (цифры только)")) 
        else:
            return await message.reply(("Длина ICCID1 должна быть из 17-19 цифр начинающихся на 89701.\nВведите ICCID1 (цифры только)"))
    await Form.next()
    await message.reply("Введите ICCID2:\n Варианты ввода: \n - 0 при отстутствии второй симки\n - Пришлите фото с изображением штрихкода или QR-кода ICCID2 (используйте сжатие изображения при посылке, не присылайте сразу несколько штрихкодов на одном фото)\n - Ввод ICCID2 вручную")

@dp.message_handler(content_types=['photo', 'text'], state=Form.iccid2)
async def get_photo_text(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        await message.photo[-1].download('test.jpg')
        img = cv2.imread('test.jpg')
        decoded_objects = pyzbar.decode(img)
        if decoded_objects:
            for obj in decoded_objects:
                string = obj.data.decode()
                string = string.replace('-', '')
                items = [
                iccid.group()
                for iccid in re.finditer(r"(89701)([0-9]{12,15})", string)
                ]
                if (string in items):
                    async with state.proxy() as data:
                        if data['iccid1'] == string:
                            return await message.reply((f"ICCID2 {string} не уникален.\nВведите ICCID2 (цифры только)"))
                        else:
                            if doublet('iccid', string):
                                data['iccid2'] = string
                            else:
                                return await message.reply((f"ICCID2 {string} не уникален.\nВведите ICCID2 (цифры только)"))
                else:
                    return await message.reply(("Длина ICCID2 должна быть из 17-19 цифр начинающихся на 89701.\nВведите ICCID2 (цифры только)"))
        else:
            return await message.reply("Введите ICCID2")
    elif message.content_type == 'text':     
        items = [
        iccid.group()
        for iccid in re.finditer(r"(89701)([0-9]{12,15})", message.text)
        ]
        if (message.text in items) or (message.text in "0"):
            async with state.proxy() as data:
                if (message.text == "0"):
                    data['iccid2'] = None
                else:
                    if data['iccid1'] == message.text:
                            return await message.reply((f"ICCID2 {message.text} не уникален.\nВведите ICCID2 (цифры только)"))
                    else:
                        if doublet('iccid', message.text):
                            data['iccid2'] = message.text
                        else:
                            return await message.reply((f"ICCID2 {message.text} не уникален.\nВведите ICCID2 (цифры только)"))
        else:
            return await message.reply(("ICCID2 должен быть из 17-19 цифр начинающихся на 89701 или 0 при отстутствии второй симки.\nВведите ICCID2 (цифры только)"))
    await Form.next()
    await message.reply(("Введите широту и долготу\n Варианты ввода: \n - Пришлите фото (документ) с метаданными места съемки (Не используйте сжатие изображения при посылке !!!)\n - Пришлите геопозицию Телеграм выбрав место установки на карте \n - Введите широту и долготу вручную (53.0000 36.0000)"))

@dp.message_handler(content_types=['document', 'text', 'location'], state=Form.geo)
async def download_document(message: types.Message, state: FSMContext):
    if message.content_type == 'document':
        output = BytesIO()
        await message.document.download(destination = output)
        output.getvalue()
        image = Image(output)   
        def coordinates(coordinates, coordinates_ref):
            decimal_degrees = coordinates[0] + coordinates[1] / 60 + coordinates[2] / 3600    
            if coordinates_ref == "S" or coordinates_ref == "W":
                decimal_degrees = -decimal_degrees
            return decimal_degrees
        latitude = coordinates(image.gps_latitude, image.gps_latitude_ref)
        longitude = coordinates(image.gps_longitude, image.gps_longitude_ref)
        async with state.proxy() as data:
            data['latitude'] = latitude
            data['longitude'] = longitude
    elif message.content_type == 'location':       
        async with state.proxy() as data:
            data['latitude'] = message.location.latitude
            data['longitude'] = message.location.longitude
    elif message.content_type == 'text':     
        async with state.proxy() as data:
            geo = message.text.split()
            geo[0] = geo[0].replace(',', '')
            if isfloat(geo[0]) and isfloat(geo[1]):
                data['latitude'] = geo[0]
                data['longitude'] = geo[1]
            else:       
                return await message.reply("Введите долготу и широту в виде чисел с точками. (запятые не допускаются)")
    await Form.next()
    await bot.send_location(message.chat.id, data['latitude'], data['longitude'])
    await message.reply("Введите номер заявки:\n Пример: \n Э-24-00-132465/522/Ю8\n Ю8-24-302-220132(425135)\n Тех учет")

@dp.message_handler(content_types=['text'], state=Form.number_task)
async def get_text_number_task(message: types.Message, state: FSMContext):
    if message.content_type == 'text':     
        async with state.proxy() as data:
            if (message.text == "0"):
                data['number_task'] = None
            else:
                data['number_task'] = message.text
    else:
        return await message.reply(("Номер заявки вводится вручную.\n Введите номер заявки или 0 при его отстутствии"))
    await Form.next()
    await message.reply("Введите дату монтажа (2024-08-19)")   

@dp.message_handler(content_types=['text'], state=Form.montag)
async def get_photo_text(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        async with state.proxy() as data:
            try:
                current_date = datetime.today()
                past_date = current_date - relativedelta(years=5)
                future_date = current_date + relativedelta(years=1)
                input_date = parse(message.text)
                if (input_date>past_date) and (input_date<future_date):
                    data['montag'] = input_date
                else:
                    return await message.reply('Не верный формат даты, необходимо ГГГГ-ММ-ДД')
            except ValueError:
                return await message.reply('Не верный формат даты, необходимо ГГГГ-ММ-ДД')
    await Form.next()   
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("on", "off")
    await message.reply("Состояние питания?", reply_markup=markup)

@dp.message_handler(lambda message: message.text not in ["on", "off"], state=Form.power)
async def process_power_invalid(message: types.Message):
    return await message.reply("Плохое состояние. Введите on или off.")

@dp.message_handler(state=Form.power)
async def process_power(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['power'] = message.text
        data['user_id'] = message.from_user.id
        data['username'] = message.from_user.username
        data['first_name'] = message.from_user.first_name
        data['last_name'] = message.from_user.last_name      
        markup = types.ReplyKeyboardRemove()
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text("*Номер ПУ:*", data['number_meter']),
            md.text("*IMEI:*", data['imei']),
            md.text("*ICCID1:*", data['iccid1']),
            md.text("*ICCID2:*", data['iccid2']),
            md.text("*latitude:*", data['latitude']),
            md.text("*longitude:*", data['longitude']),
            md.text("*number_task:*", data['number_task']),
            md.text("*montag:*", data['montag']),
            md.text("*power:*", data['power']),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )  
    await Form.next()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(
            "✅Сохранить",
            "❌Выйти")
    await message.reply("Все верно?", reply_markup=markup)

@dp.message_handler(state=Form.end)
async def process_end(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['end'] = message.text   
    if  data['end'] == "✅Сохранить": 
        if data['power'] == 'on':
            p = 1
        if data['power'] == 'off':
            p = 0
        dt_now = datetime.now()
        stmt = insert(Meter).values(
            user_id = data['user_id'],
            username = data['username'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            number_meter = data['number_meter'],
            imei = data['imei'],
            iccid1 = data['iccid1'],
            iccid2 = data['iccid2'],
            latitude = data['latitude'],
            longitude = data['longitude'],
            number_task = data['number_task'],
            montag = data['montag'],
            power = p,
            created_on = dt_now,
            state_meter = None)
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
        await state.finish()
        await message.reply('Ok', reply_markup=types.ReplyKeyboardRemove())
        message_text = str(message.text)
        list_param_log_cmd = [0, 0, message.from_user.id, message.from_user.mention, message.from_user.full_name]
        list_param_log_cmd[0] = start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name)
        list_param_log_cmd[1] = write_log(start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name), 'input', message_text)
        print_format_log_cmd(list_param_log_cmd, 'end', message_text)
    elif  data['end'] == "❌Выйти":
        current_state = await state.get_state()
        if current_state is None:
            return
        message_text = str(message.text)
        list_param_log_cmd = [0, 0, message.from_user.id, message.from_user.mention, message.from_user.full_name]
        list_param_log_cmd[0] = start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name)
        list_param_log_cmd[1] = write_log(start_user(message.from_user.id, message.from_user.mention, message.from_user.full_name), 'input', message_text)
        textout = """Отменено на состояние {current_st}"""
        textout = textout.format(current_st=current_state)
        print_format_log_cmd(list_param_log_cmd, 'in', textout)
        await state.finish()
        await message.reply('Ok', reply_markup=types.ReplyKeyboardRemove())

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def doublet(column, value):
    if (column == 'iccid'):
        stmt = f"SELECT COUNT(*) FROM meter WHERE iccid1 ='{value}' or iccid2 ='{value}' and state_meter IS null;" 
    else:
        stmt = f"SELECT COUNT(*) FROM meter WHERE {column} ='{value}' and state_meter IS null;"
    with engine.connect() as conn:
        result = conn.execute(text(stmt))
        res=result.fetchone()[0]
    try:
        if res == 0:
            return True
    except ValueError:
        return False
    