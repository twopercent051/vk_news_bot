from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMGroups(StatesGroup):
    adding = State()

class FSMFriends(StatesGroup):
    adding = State()

