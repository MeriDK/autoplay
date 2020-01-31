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
bot_zhaba = 'jabkvabot'

time_to_walk = 1
time_to_sleep = 1
time_to_eat = 12 * 3600 + 60    # 12 hours after code start
time_update_clan = 4 * 3600 + 60    # each hour
eat_counter = 2

clan_arena_check = True
busy_check = False
clan_check = False


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

    global busy_check
    while busy_check:
        await asyncio.sleep(60)

    busy_check = True
    log.log('Went for a walk')

    await send(['⛩ Городские ворота', '🐾 Прогулка'])
    await send('🌲 В мрачных землях 🌲', delay=10)
    await send(['🐾 Прогулка', '🌲 В мрачных землях 🌲', '◀️ Назад'])

    busy_check = False
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

    global busy_check
    while busy_check:
        await asyncio.sleep(60)

    busy_check = True
    log.log('Went to sleep and get daily bonus')

    await send(['🏯 Квартал героев', '🏠 Дом Героя'])
    await send('🛏 Поспать', delay=10)
    await send(['◀️ Назад', '◀️ Назад', '🏪 Торговый квартал', '🎲 Игорный дом', '🎁 Ежедневный бонус',
                '◀️ Назад', '◀️ Назад'])

    busy_check = False
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

    global busy_check
    while busy_check:
        await asyncio.sleep(60)

    busy_check = True

    global eat_counter
    await send(['🏯 Квартал героев', '🏠 Дом Героя', f'🍗 Перекусить (Осталось {eat_counter} раз)'])
    await send(['◀️ Назад', '◀️ Назад'], delay=2)

    eat_counter = 1 if eat_counter == 2 else 1
    busy_check = False

    await asyncio.create_task(eat())


# clan arena
@client.on(events.NewMessage(from_users=bot_username, pattern=r'Игрок .+ приглашает тебя принять'))
async def arena_handler(event):
    global clan_arena_check
    if clan_arena_check:
        clan_arena_check = False

        await asyncio.sleep(3)
        res = await event.click()
        if res.message is None:
            await asyncio.sleep(3600)     # sleep for 1 hour

        clan_arena_check = True


# busy check for dungeons
@client.on(events.NewMessage(from_users=bot_username, pattern=r'Пожалуйста, ждите...'))
async def arena_handler(event):
    global busy_check
    busy_check = True


# busy check for dungeons
@client.on(events.NewMessage(from_users=bot_username, pattern=r'(Вы выиграли|Вам возвращена энергия|Отменено!)'))
async def arena_handler(event):
    global busy_check
    busy_check = False


# busy check for arena
@client.on(events.NewMessage(from_users=bot_username, pattern=r'Ваш противник:'))
async def arena_handler(event):
    global busy_check
    busy_check = True


# busy check for arena
@client.on(events.NewMessage(from_users=bot_username, pattern=r'(За победу ты награждаешься|За участие ты получил)'))
async def arena_handler(event):
    global busy_check
    busy_check = False


# clan users updater
async def clan_update():
    await asyncio.sleep(time_update_clan)

    global busy_check
    while busy_check:
        await asyncio.sleep(60)
    busy_check = True

    global clan_check
    clan_check = True

    await send(['⛩ Городские ворота', '👥 Клановая крепость'])
    await asyncio.sleep(10)
    await send('◀️ Назад')

    busy_check = False
    clan_check = False

    await asyncio.create_task(clan_update())


@client.on(events.NewMessage(from_users=bot_username, pattern=r'⚔️ Жабодержава'))
async def walk_handler(event):
    if clan_check:
        await asyncio.sleep(1)
        await event.click()
        await asyncio.sleep(1)
        msg = await client.get_messages(bot_username, ids=event.message.id)
        await msg.forward_to(bot_zhaba)
        while not (await msg.buttons[0][1].click()).message:
            await asyncio.sleep(1)
            msg = await client.get_messages(bot_username, ids=event.message.id)
            await msg.forward_to(bot_zhaba)


async def main():
    await set_time()

    await asyncio.gather(
        walk(),
        sleep_and_bonus(),
        eat(),
        clan_update()
    )

with client:
    client.loop.run_until_complete(main())
    log.log('Disconnected')

