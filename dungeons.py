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
move_phrases = ['Сделать шаг', 'Подойти к боссу', 'Отойти немного', 'Перепрыгнуть лужу лавы']
die = '🌀🌀 БЕЗДЕЙСТВУЙТЕ ИЛИ УМРИТЕ 🌀🌀'

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


async def check_in_answer(buttons):
    for button in [button for row in buttons for button in row]:
        if 'в ответ' in button.text:
            await button.click()
            log.log(button.text)
            return True
    return False


@client.on(events.NewMessage(from_users=bot_username, pattern=r'Твой ход, 🐸MeriDK'))
async def main(event):
    await asyncio.sleep(1)
    buttons = await event.get_buttons()

    # check for phrase with 'in answer'
    if not await check_in_answer(buttons):
        move = False

        # check for possibility to move
        for button in [button for row in buttons for button in row]:
            if check_move_phrase(button.text):
                await button.click()
                log.log(button.text)
                move = True

        # attack boss
        if not move:
            for button in [button for row in buttons for button in row]:
                if check_boss_phrase(button.text):
                    await button.click()
                    log.log(button.text)


client.start()
client.run_until_disconnected()
