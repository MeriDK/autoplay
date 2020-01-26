import asyncio
from telethon import TelegramClient, events
import logging
from log import Log
from config import API_ID, API_HASH

# updates need not to crush
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# init logger
log = Log('dungeon_log.txt')

# log in
client = TelegramClient('dungeons', API_ID, API_HASH)
log.log('Connected')

# code info
bot_username = 'WOD_dungeon_bot'

boss_phrases = ['гиганта', 'верзилу', 'чудовище', 'чудище', 'монстра']
move_phrases = ['Сделать шаг', 'Подойти к боссу', 'Отойти', 'Перепрыгнуть лужу лавы']

check_die = False


def check_boss_phrase(text):
    for phrase in boss_phrases:
        if phrase in text:
            return True
    return False


def check_move_phrase(text):
    for phrase in move_phrases:
        if phrase in text:
            return True
    return False


async def get_buttons(event):
    await asyncio.sleep(1)
    buttons = await event.get_buttons()
    buttons = [button for row in buttons for button in row]
    return buttons


@client.on(events.NewMessage(from_users=bot_username, pattern=r'🌀 Отречение 🌀\nТвой ход, 🐸MeriDK'))
async def main(event):
    buttons = await get_buttons(event)

    for button in buttons:
        if not check_boss_phrase(button.text):
            await button.click()
            log.log(button.text)
            break


@client.on(events.NewMessage(from_users=bot_username, pattern=r'😡 Твои ноги горят 😡\nТвой ход, 🐸MeriDK'))
async def main(event):
    buttons = await get_buttons(event)

    for button in buttons:
        if check_move_phrase(button.text):
            await button.click()
            log.log(button.text)


@client.on(events.NewMessage(from_users=bot_username, pattern=r'Твой ход, 🐸MeriDK'))
async def main(event):
    buttons = await get_buttons(event)

    # response
    for button in buttons:
        if 'в ответ' in button.text:
            await button.click()
            log.log(button.text)
            return

    for button in buttons:
        if check_boss_phrase(button.text):
            await button.click()
            log.log(button.text)


client.start()
client.run_until_disconnected()
