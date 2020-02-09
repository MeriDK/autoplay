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

# bot info
bot_username = 'WorldDogs_bot'
bot_zhaba = 'jabkvabot'

time = {
    'walk': 1,
    'sleep_and_bonus': 120,
    'eat': 12 * 3600,
    'clan_update': 4 * 3600
}

clan_arena_check = False
busy_check = False
clan_update_check = False


# function to send messages
async def send(msgs, username=bot_username, delay=1):
    if isinstance(msgs, str):
        msgs = [msgs]

    for msg in msgs:
        await client.send_message(username, msg)
        log.log(msg)
        await asyncio.sleep(delay)


# function to count time
def set_time(raw_text):
    msg = raw_text.split(':')[1:]
    return sum([int(msg[i]) * 60 ** (2 - i) for i in range(len(msg))]) + 60


# busy func
async def run_func(function):
    global busy_check
    while busy_check:
        await asyncio.sleep(60)
    busy_check = True
    log.log('Busy check True')

    await function()

    busy_check = False
    log.log('Busy check False')


# walk
@client.on(events.NewMessage(from_users=bot_username, pattern=r'^Ты уже недавно гулял!'))
async def walk_handler(event):
    time['walk'] = set_time(event.raw_text)
    log.log(f'Next walk in {time["walk"]} s')


async def walk_func():
    log.log('Went for a walk')

    await send(['⛩ Городские ворота', '🐾 Прогулка'])
    await send('🌲 В мрачных землях 🌲', delay=10)
    await send(['🐾 Прогулка', '🌲 В мрачных землях 🌲', '◀️ Назад'])


async def walk():
    await asyncio.sleep(time['walk'])
    await run_func(walk_func)
    await asyncio.create_task(walk())


# sleep and bonus
@client.on(events.NewMessage(from_users=bot_username, pattern=r'^Ты уже недавно отдыхал!'))
async def sleep_and_bonus_handler(event):
    time['sleep_and_bonus'] = set_time(event.raw_text)
    log.log(f'Next sleep in {time["sleep_and_bonus"]} s')


async def sleep_and_bonus_func():
    log.log('Went to sleep and get daily bonus')

    await send(['🏯 Квартал героев', '🏠 Дом Героя'])
    await send('🛏 Поспать', delay=10)
    await send(['◀️ Назад', '◀️ Назад', '🏪 Торговый квартал', '🎲 Игорный дом', '🎁 Ежедневный бонус',
                '◀️ Назад', '◀️ Назад'])


async def sleep_and_bonus():
    await asyncio.sleep(time['sleep_and_bonus'])
    await run_func(sleep_and_bonus_func)
    await asyncio.create_task(sleep_and_bonus())


# eat
async def eat_func():
    await send(['🏯 Квартал героев', '🏠 Дом Героя'])
    msg = (await client.get_messages(bot_username))[0]
    await send((await msg.get_buttons())[0][0].text)
    await send(['◀️ Назад', '◀️ Назад'], delay=2)


async def eat():
    await asyncio.sleep(time['eat'])
    await run_func(eat_func)
    await asyncio.create_task(eat())


# clan update
@client.on(events.NewMessage(from_users=bot_username, pattern=r'⚔️ Жабодержава'))
async def clan_update_handler(event):
    if clan_update_check:
        await asyncio.sleep(1)
        await event.click()
        await asyncio.sleep(1)
        msg = await client.get_messages(bot_username, ids=event.message.id)
        await msg.forward_to(bot_zhaba)
        while not (await msg.buttons[0][1].click()).message:
            await asyncio.sleep(1)
            msg = await client.get_messages(bot_username, ids=event.message.id)
            await msg.forward_to(bot_zhaba)


async def clan_update_func():
    global clan_update_check
    clan_update_check = True

    await send(['⛩ Городские ворота', '👥 Клановая крепость'])
    await asyncio.sleep(10)
    await send('◀️ Назад')

    clan_update_check = False


async def clan_update():
    await asyncio.sleep(time['clan_update'])
    await run_func(clan_update_func)
    await asyncio.create_task(clan_update())


# clan arena
@client.on(events.NewMessage(from_users=bot_username, pattern=r'Игрок .+ приглашает тебя принять'))
async def arena_handler(event):
    global clan_arena_check
    if not clan_arena_check:
        clan_arena_check = True

        await asyncio.sleep(3)
        res = await event.click()
        if res.message is None:
            await asyncio.sleep(3600)  # sleep for 1 hour

        clan_arena_check = False


# busy check True
@client.on(events.NewMessage(from_users=bot_username,
                             pattern=r'(Пожалуйста, ждите...|Ваш противник:|Отряд успешно собран)'))
async def busy_handler_t(event):
    global busy_check
    busy_check = True


# busy check False
@client.on(events.NewMessage(from_users=bot_username,
                             pattern=r'(Вы выиграли|Вам возвращена энергия|Отменено!|За победу ты |За участие ты )'))
async def busy_handler_f(event):
    global busy_check
    busy_check = False


async def main():
    await asyncio.gather(
        walk(),
        sleep_and_bonus(),
        eat(),
        clan_update()
    )


with client:
    client.loop.run_until_complete(main())
    log.log('Disconnected')

