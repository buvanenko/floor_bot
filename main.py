# Бот для вывода флора коллекции в чатик

import os
import asyncio

from dotenv import load_dotenv
from typing import Tuple

from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import CommandRule
from vkbottle.tools import PhotoMessageUploader

import floor
import keyboards
import admin
import chart

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


bot = Bot(token=os.getenv("VK_API_KEY"))
uploader = PhotoMessageUploader(bot.api, generate_attachment_strings=True)

schedule_peer_id = 0

# Вывести актуальный флор
@bot.on.message(text="/флор")
async def now_handler(message: Message):
    bot_message = await floor.get()
    if message.peer_id == message.from_id:
        raw_data = await floor.get_raw()
        buf = chart.generate(raw_data)
        attachment = await uploader.upload(buf, peer_id=message.peer_id)
        await message.answer(
            bot_message,
            attachment=attachment, 
            keyboard=keyboards.market_links
            )
    else:
        await message.answer(bot_message, keyboard=keyboards.market_links)

# Отправлять флор каждые n минут
@bot.on.message(CommandRule("старт", ['/'], 1))
async def schedule_handler(message: Message, args: Tuple[str]):
    is_admin = await admin.check(bot, message.peer_id, message.from_id)
    if is_admin == False:
        await message.answer("У вас нет доступа к этой команде")
        return
    global schedule_peer_id # позор мне за глобальную переменную
    if schedule_peer_id == message.peer_id:
        await message.answer("Бот уже запущен")
        return
    schedule_peer_id = message.peer_id
    while schedule_peer_id == message.peer_id:
        bot_message = await floor.get()
        await message.answer(bot_message, keyboard=keyboards.market_links)
        await asyncio.sleep(int(args[0])*60)

# Остановить отправку флора
@bot.on.message(text="/стоп")
async def stop_handler(message: Message):
    is_admin = await admin.check(bot, message.peer_id, message.from_id)
    if is_admin == False:
        await message.answer("У вас нет доступа к этой команде")
        return
    global schedule_peer_id
    schedule_peer_id = 0
    await message.answer("Бот остановлен")

@bot.on.message(text="/admin")
async def admin_handler(message: Message):
    is_admin = await admin.check(bot, message.peer_id, message.from_id)
    if is_admin == False:
        await message.answer("У вас нет доступа к этой команде")
        return
    await message.answer("Вы администратор")

if __name__ == "__main__":
    bot.run_forever()