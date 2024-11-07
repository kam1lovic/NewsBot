from aiogram import Router, F
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.i18n import gettext as _
from sqlalchemy import select

from bot.buttons.inline import organization_type
from bot.buttons.keyboard import select_web_or_channel
from bot.states import CategorySelection
from database.base import db
from database.models import User, Organization

# Replace `PreviousState` with the desired state you want to transition back to

organ_router = Router()


@organ_router.callback_query(F.data.startswith("organization_"))
async def process_organization_type(callback_query: CallbackQuery):
    organization_type = callback_query.data.split("_")[1]

    user = await User.get(callback_query.from_user.id)
    user_language = user.language

    if user_language == 'en':
        organizations_query = select(Organization.id, Organization.name_en).where(
            Organization.type_en == organization_type)
    elif user_language == 'ru':
        organizations_query = select(Organization.id, Organization.name_ru).where(
            Organization.type_ru == organization_type)
    else:
        organizations_query = select(Organization.id, Organization.name_uz).where(
            Organization.type_uz == organization_type)

    organizations_result = await db.execute(organizations_query)
    organizations = organizations_result.all()

    buttons = [
        InlineKeyboardButton(text=name, callback_data=f"name_{org_id}")
        for org_id, name in organizations
    ]

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)])

    back_button = InlineKeyboardButton(text=_("Orqaga"), callback_data="back_to_types")
    keyboard_markup.inline_keyboard.append([back_button])

    await callback_query.message.edit_text(
        _("Tashkilot nomini tanlang:"),
        reply_markup=keyboard_markup
    )


@organ_router.callback_query(F.data.startswith("name_"))
async def process_organization_name(callback_query: CallbackQuery):
    organization_id = int(callback_query.data.split("_")[1])

    user = await User.get(callback_query.from_user.id)
    user_language = user.language

    if user_language == 'ru':
        organization_query = select(Organization.original_name, Organization.phone).where(
            Organization.id == organization_id)
    else:
        organization_query = select(Organization.latin_name, Organization.phone).where(
            Organization.id == organization_id
        )

    organization_result = await db.execute(organization_query)
    organization_info = organization_result.first()

    if organization_info:
        name, phone = organization_info
        await callback_query.message.answer(
            f"👤: {name}\n☎️: {phone}"
        )
    else:
        await callback_query.answer(_("Tashkilot topilmadi."), show_alert=True)


@organ_router.callback_query(F.data == "back_to_types")
async def back_to_types(callback_query: CallbackQuery):
    user = await User.get(callback_query.from_user.id)
    user_language = user.language
    button = await organization_type(user_language)

    await callback_query.message.edit_text(
        _("Davlat organlari bilan bog'lanish tanlandi!"),
        reply_markup=button
    )


@organ_router.callback_query(lambda c: c.data == "back")
async def handle_back_button(callback_query: CallbackQuery, state: FSMContext):
    user = await User.get(callback_query.from_user.id)
    user_language = user.language
    button = await select_web_or_channel(lang_code=user_language)
    await callback_query.answer()
    await state.set_state(CategorySelection.select_web_or_telegram)
    await callback_query.message.answer(
        _("Siz orqaga qaytdingiz ⤵️"),
        reply_markup=button
    )
