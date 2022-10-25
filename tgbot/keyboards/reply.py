from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_groups_show = KeyboardButton('**Показать группы**')
button_groups_edit = KeyboardButton('**Редактировать список групп**')
button_friends_show = KeyboardButton('**Показать друзей**')
button_friends_edit = KeyboardButton('**Редактировать список друзей**')

button_case_show = ReplyKeyboardMarkup(resize_keyboard=True).add(button_groups_show).add(button_friends_show)
button_case_groups_edit = ReplyKeyboardMarkup(resize_keyboard=True).add(button_groups_edit)
button_case_friends_edit = ReplyKeyboardMarkup(resize_keyboard=True).add(button_friends_edit)