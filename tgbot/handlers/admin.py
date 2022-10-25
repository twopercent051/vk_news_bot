from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold

import tgbot.keyboards.reply as reply
from tgbot.middlewares import vk_request
from tgbot.misc.states import FSMGroups, FSMFriends

import json


async def admin_start(message: Message):
    text = [
        'Здравствуйте! Вы вошли с правами администратора. Бот может перенаправлять новостную ленту из ВКонтакте.',
        'Бот присылает новости только от тех групп и друзей, которые находятся в списке. Для просмотра и редактирования списка',
        'нажмите клавишу ниже'
    ]
    await message.answer(' '.join(text), reply_markup=reply.button_case_show)

async def show_groups(message: Message):
    text = ['Пожалуйста, подождите...']
    groups_vk_name_list = [
        hbold('Список групп, на которые вы подписаны ВКонтакте:'),
        ''
    ]
    groups_file_name_list = [
        hbold('Список групп, из которых вы получаете оповещения:'),
        ''
    ]
    await message.answer(' '.join(text))
    groups_vk_list = await vk_request.get_groups()
    with open('groups.json', encoding='utf-8') as file:
        groups_file_list = json.load(file)
    for item_vk in groups_vk_list:
        group_vk_name = item_vk['name']
        groups_vk_name_list.append(group_vk_name)
    for item_file in groups_file_list:
        group_file_name = item_file['name']
        groups_file_name_list.append(group_file_name)
    await message.answer('\n'.join(groups_vk_name_list), reply_markup=reply.button_case_groups_edit)
    await message.answer('\n'.join(groups_file_name_list))


async def edit_groups_start(message: Message):
    text = [
        'Скопируйте через ENTER те группы, по которым хотите получать информацию в новостной ленте',
        'ВНИМАНИЕ! Список будет полностью перезаписан без предупреждения'
    ]
    await message.answer(' '.join(text))
    await FSMGroups.adding.set()


async def edit_groups_proc(message: Message, state: FSMGroups):
    new_group_list = str(message.text).strip().split('\n')
    get_dict = await vk_request.get_groups()
    new_group_dict = []
    for item in get_dict:
        if item['name'] in new_group_list:
            new_group_dict.append(item)
    with open('groups.json', 'w', encoding='utf-8') as file:
        json.dump(new_group_dict, file, indent=4, ensure_ascii=False)
    text = [
        'Новый список групп записан. Проверьте список'
    ]
    await message.answer(''.join(text), reply_markup=reply.button_case_show)
    await state.finish()


async def show_friends(message: Message):
    text = ['Пожалуйста, подождите...']
    friends_vk_name_list = [
        hbold('Список друзей, на которые вы подписаны ВКонтакте:'),
        ''
    ]
    friends_file_name_list = [
        hbold('Список друзей, от которых вы получаете оповещения:'),
        ''
    ]
    await message.answer(' '.join(text))
    friends_vk_list = await vk_request.get_friends()
    with open('friends.json', encoding='utf-8') as file:
        friends_file_list = json.load(file)
    for item_vk in friends_vk_list:
        friends_vk_first_name = item_vk['first_name']
        friends_vk_last_name = item_vk['last_name']
        friends_vk_name_list.append(f'{friends_vk_first_name} {friends_vk_last_name}')

    for item_file in friends_file_list:
        try:
            friends_file_name = f"{item_file['first_name']} {item_file['last_name']}"
            friends_file_name_list.append(friends_file_name)
        except:
            friends_file_name_list.append('')
    await message.answer('\n'.join(friends_vk_name_list), reply_markup=reply.button_case_friends_edit)
    await message.answer('\n'.join(friends_file_name_list))


async def edit_friends_start(message: Message):
    text = [
        'Скопируйте через ENTER тех друзей, по которым хотите получать информацию в новостной ленте',
        'ВНИМАНИЕ! Список будет полностью перезаписан без предупреждения'
    ]
    await message.answer(' '.join(text))
    await FSMFriends.adding.set()


async def edit_friends_proc(message: Message, state: FSMFriends):
    new_friends_list = str(message.text).strip().split('\n')
    get_dict = await vk_request.get_friends()
    new_friends_dict = []
    for item in get_dict:
        if f"{item['first_name']} {item['last_name']}" in new_friends_list:
            new_friends_dict.append(item)
    with open('friends.json', 'w', encoding='utf-8') as file:
        json.dump(new_friends_dict, file, indent=4, ensure_ascii=False)
    text = [
        'Новый список друзей записан. Проверьте список'
    ]
    await message.answer(''.join(text), reply_markup=reply.button_case_show)
    await state.finish()



def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)

    dp.register_message_handler(show_groups, Text(equals='**Показать группы**', ignore_case=True), is_admin=True)
    dp.register_message_handler(edit_groups_start, Text(equals='**Редактировать список групп**', ignore_case=True), is_admin=True)
    dp.register_message_handler(edit_groups_proc, content_types=['text'], state=FSMGroups.adding)

    dp.register_message_handler(show_friends, Text(equals='**Показать друзей**', ignore_case=True), is_admin=True)
    dp.register_message_handler(edit_friends_start, Text(equals='**Редактировать список друзей**', ignore_case=True), is_admin=True)
    dp.register_message_handler(edit_friends_proc, content_types=['text'], state=FSMFriends.adding)
