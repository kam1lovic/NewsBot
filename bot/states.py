from aiogram.fsm.state import StatesGroup, State


class CategorySelection(StatesGroup):
    select_web_or_telegram = State()
    web_selected = State()
    telegram_selected = State()


class Profile(StatesGroup):
    profile = State()


class AddCategoryState(StatesGroup):
    waiting_for_category_name = State()
    waiting_for_category_emoji = State()


class AddSiteState(StatesGroup):
    waiting_for_site_url = State()


class SetLanguage(StatesGroup):
    language = State()


class AddChannelState(StatesGroup):
    waiting_for_channel_name = State()
    waiting_for_channel_username = State()
