# bot/handlers/add_category_router.py

import logging

import emoji
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.buttons.keyboard import add_site_or_category
from bot.states import AddCategoryState, Profile
from bot.utils import add_category

add_category_router = Router()

PROHIBITED_EMOJI = ['🖕🏿', '🖕🏻', '🖕🏽', '🖕🏾', '🖕', '🍑', '🍆', '🍌']

@add_category_router.message(AddCategoryState.waiting_for_category_name)
async def receive_category_name(message: Message, state: FSMContext):
    category_name = message.text.strip()
    logging.debug(f"Received category name: {category_name}")

    await state.update_data(category_name=category_name)
    await message.answer(_("Kategoriya uchun emoji yuboring:"))
    await state.set_state(AddCategoryState.waiting_for_category_emoji)


@add_category_router.message(AddCategoryState.waiting_for_category_emoji)
async def receive_category_emoji(message: Message, state: FSMContext):
    if not message.text:
        await message.answer(_("Iltimos, emoji yuboring."))
        return

    emoji_input = message.text.strip()
    logging.debug(f"Received emoji: {emoji_input}")

    if not all(emoji.is_emoji(char) for char in emoji_input):
        await message.answer(_("Iltimos, haqiqiy emoji yuboring."))
        return

    if any(char in PROHIBITED_EMOJI for char in emoji_input):
        await message.answer(_("Bu emoji kiritilishi mumkin emas. Iltimos, boshqa emoji kiriting."))
        return

    data = await state.get_data()
    category_name = data.get('category_name')
    user_id = message.from_user.id
    logging.debug(f"Adding category with name: {category_name}, emoji: {emoji_input}, user_id: {user_id}")

    result_message = await add_category(name=category_name, emoji=emoji_input, user_id=user_id)
    await message.answer(result_message)

    btn = await add_site_or_category()
    await state.set_state(Profile.profile)
    await message.answer(_("Siz profil bo'limiga qaytdingiz. Iltimos, boshqa amalni tanlang."), reply_markup=btn)
