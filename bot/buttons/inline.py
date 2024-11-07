from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from sqlalchemy import select

from database.base import db
from database.models import Category, Organization


async def category_buttons(user_language, selected_categories=None):
    if selected_categories is None:
        selected_categories = []

    def create_button(text, category_id):
        if category_id in selected_categories:
            text = f"{text} ✅"
        return InlineKeyboardButton(text=text, callback_data=f"category_{category_id}")

    if user_language == "uz":
        name_field = Category.name_uz
    elif user_language == "ru":
        name_field = Category.name_ru
    else:
        name_field = Category.name

    query = select(Category).where(Category.dynamic_category == False)
    categories_result = await db.execute(query)
    categories = categories_result.scalars().all()

    # Kategoriyalar nomi foydalanuvchi tiliga mos ravishda tanlanadi
    buttons = [create_button(f"{category.emoji} {getattr(category, name_field.key)}", category.id) for category in categories]

    rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
    rows.append([InlineKeyboardButton(text=_("💾 Saqlash"), callback_data="save")])

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard_markup


async def organization_type(user_language):
    if user_language == 'en':
        organizations_query = select(Organization.type_en).distinct()
    elif user_language == 'ru':
        organizations_query = select(Organization.type_ru).distinct()
    else:
        organizations_query = select(Organization.type_uz).distinct()

    organizations_result = await db.execute(organizations_query)
    organizations = organizations_result.scalars().all()

    buttons = [InlineKeyboardButton(text=organization, callback_data=f"organization_{organization}") for organization in
               organizations]

    rows = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

    back_button = InlineKeyboardButton(text=_("Orqaga"), callback_data="back")
    rows.append([back_button])

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard_markup
