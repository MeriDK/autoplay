import asyncio
from telethon import TelegramClient, events
import logging
from log import Log
from config import API_ID, API_HASH

# updates need not to crush
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# init logger
log = Log('log.txt')

# log in
client = TelegramClient('bot', API_ID, API_HASH)
log.log('Connected')

# code info
bot_username = 'WorldDogs_bot'

time_to_walk = 1
time_to_sleep = 1
time_to_eat = 12 * 3600 + 60    # 12 hours after code start
eat_counter = 2


# function to send messages
async def send(msgs, username=bot_username, delay=1):
    if isinstance(msgs, str):
        msgs = [msgs]

    for msg in msgs:
        await client.send_message(username, msg)
        log.log(msg)
        await asyncio.sleep(delay)


async def set_time():
    # set time to walk
    log.log('Went to set time for next walk')
    await send(['⛩ Городские ворота', '🐾 Прогулка', '🌲 В мрачных землях 🌲', '◀️ Назад'])

    # set time to sleep and bonus
    log.log('Went to set time for next sleep')
    await send(['🏯 Квартал героев', '🏠 Дом Героя', '🛏 Поспать', '◀️ Назад', '◀️ Назад'])


# go for a walk
async def walk():
    await asyncio.sleep(time_to_walk)

    log.log('Went for a walk')

    await send(['⛩ Городские ворота', '🐾 Прогулка'])
    await send('🌲 В мрачных землях 🌲', delay=10)
    await send(['🐾 Прогулка', '🌲 В мрачных землях 🌲', '◀️ Назад'])

    await asyncio.create_task(walk())


# walk handler to set time for next walk
@client.on(events.NewMessage(from_users=bot_username, pattern=r'^Ты уже недавно гулял!'))
async def walk_handler(event):
    msg = event.raw_text.split(':')[1:]

    global time_to_walk
    time_to_walk = sum([int(msg[i]) * 60**(2 - i) for i in range(len(msg))]) + 60

    log.log(f'Next walk in {time_to_walk} s')


# go to sleep and then get bonus
async def sleep_and_bonus():
    await asyncio.sleep(time_to_sleep)

    log.log('Went to sleep and get daily bonus')

    await send(['🏯 Квартал героев', '🏠 Дом Героя'])
    await send('🛏 Поспать', delay=10)
    await send(['◀️ Назад', '◀️ Назад', '🏪 Торговый квартал', '🎲 Игорный дом', '🎁 Ежедневный бонус',
                '◀️ Назад', '◀️ Назад'])

    await asyncio.create_task(sleep_and_bonus())


# sleep handler for setting time for next sleep
@client.on(events.NewMessage(from_users=bot_username, pattern=r'^Ты уже недавно отдыхал!'))
async def sleep_handler(event):
    msg = event.raw_text.split(':')[1:]

    global time_to_sleep
    time_to_sleep = sum([int(msg[i]) * 60**(2 - i) for i in range(len(msg))]) + 60

    log.log(f'Next sleep in {time_to_sleep} s')


# go to eat
async def eat():
    await asyncio.sleep(time_to_eat)

    global eat_counter
    await send(['🏯 Квартал героев', '🏠 Дом Героя', f'🍗 Перекусить (Осталось {eat_counter} раз)'])
    await send(['◀️ Назад', '◀️ Назад]'], delay=2)

    eat_counter = 1 if eat_counter == 2 else 1

    await asyncio.create_task(eat())


async def main():
    await set_time()

    await asyncio.gather(
        walk(),
        sleep_and_bonus(),
        eat()
    )

with client:
    client.loop.run_until_complete(main())
    log.log('Disconnected')

