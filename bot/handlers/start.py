from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.buttons.keyboard import get_language_keyboard, select_web_or_channel
from bot.states import CategorySelection
from database.models import User
from database.base import db

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message):
    user_data = message.from_user.model_dump(include={"id", "first_name", "last_name", "username"})
    if not await User.get(message.from_user.id):
        await User.create(**user_data)

    await message.answer(
        "🇺🇿 Iltimos tilni tanlang:\n\n🇬🇧 Please select a language:\n\n🇷🇺 Пожалуйста, выберите язык",
        reply_markup=get_language_keyboard()
    )


@start_router.message(lambda message: message.text in ["🇬🇧 English", "🇷🇺 Русский", "🇺🇿 O'zbek"])
async def set_language(message: Message, state: FSMContext):
    if message.text == "🇬🇧 English":
        lang_code = 'en'
    elif message.text == "🇷🇺 Русский":
        lang_code = 'ru'
    else:
        lang_code = 'uz'

    user = await User.get(message.from_user.id)
    if user:
        user.language = lang_code
        db.add(user)  # Foydalanuvchini sessiyaga qo'shamiz
        await db.commit()  # O'zgarishlarni bazaga saqlaymiz

    # Davlatni (locale) saqlaymiz
    await state.set_data({'locale': lang_code})
    button = await select_web_or_channel(lang_code)
    translated_message = _("Til muvaffaqiyatli o'rnatildi!\n\nIltimos tugmalardan birini tanlang⤵️", locale=lang_code)

    await state.set_state(CategorySelection.select_web_or_telegram)
    await message.answer(translated_message, reply_markup=button)
