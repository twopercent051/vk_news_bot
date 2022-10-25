from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text

from tgbot.keyboards.reply import button_case
from tgbot.misc.states import FSMAPI, FSMFriends

import json

async def user_start(message: Message):
    text = [
        'Приветствую! Чтобы бот сканировал комментарии ВК, нужно загрузить API-токен',
        'Если токен загружен, вы можете редактировать список друзей',
        'Для этого нажмите соответствующую клавишу'
    ]
    await message.answer(' '.join(text), reply_markup=button_case)


async def edit_api_start(message: Message):
    text = [
        'Введите API-токен приложения',
        'ВНИМАНИЕ! После отправки этого сообщение API-токен будет перезаписан безвозвратно'
    ]
    await FSMAPI.adding.set()
    await message.answer(' '.join(text))


async def edit_api_proc(message: Message):
    vk_token = list(str(message.text).strip())
    with open('vk_config.json', 'w', encoding='utf-8') as file:
        json.dump(vk_token, file, indent=4, ensure_ascii=False)
    await FSMAPI.finish()


async def edit_friends_start(message: Message):
    text = [
        'Загружаем список друзей. Это может занять время. Скопируйте список, удалите ненужные позиции и отправьте в',
        'бот список, который хотите сканировать. ВАЖНО! Список будет полностью перезаписан. Между позициями должен',
        'стоять ENTER'
        ]
    await message.answer(' '.join(text))



def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(edit_friends, Text(equals='**Редактировать друзей**', ignore_case=True), state='*')
