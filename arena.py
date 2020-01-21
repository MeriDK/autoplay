import asyncio
from telethon import TelegramClient, events
import logging
from config import API_ID, API_HASH
from log import Log

# set how many times you want to go to arena
arena_counter = 1

# updates need not to crush
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# init logger
log = Log('log.txt')

# log in
client = TelegramClient('arena', API_ID, API_HASH)
log.log('Connected')

# code info
bot_username = 'WorldDogs_bot'


# function to send messages
async def send(msgs, username=bot_username, delay=1):
    if isinstance(msgs, str):
        msgs = [msgs]

    for msg in msgs:
        await client.send_message(username, msg)
        log.log(msg)
        await asyncio.sleep(delay)


# go to arena
async def arena():
    log.log('Went to arena')

    await send('⛩ Городские ворота')
    await send('⚔️ Арена', delay=3)
    await send(['⚔️ Войти на арену' for _ in range(arena_counter)], delay=15)
    await send('◀️ Назад')
    await send('⚔️ Арена', delay=3)
    await send(['◀️ Назад', '◀️ Назад'])


# arena handler to click buttons
@client.on(events.NewMessage(from_users=bot_username, pattern=r'(🧙‍♂️Сражайся на арене|Еще один шаг|Ваш противник)'))
async def arena_handler(event):
    await asyncio.sleep(1)
    await event.click()


async def main():
    await arena()


with client:
    client.loop.run_until_complete(main())
