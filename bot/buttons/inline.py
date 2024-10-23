from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from sqlalchemy import select

from database.base import db
from database.models import Category


async def category_buttons(user_id, selected_categories=None):
    if selected_categories is None:
        selected_categories = []

    def create_button(text, category_id):
        if category_id in selected_categories:
            text = f"{text} ✅"
        return InlineKeyboardButton(text=text, callback_data=f"category_{category_id}")

    query = select(Category).where((Category.user_id == None) | (Category.user_id == user_id))
    categories_result = await db.execute(query)
    categories = categories_result.scalars().all()

    buttons = [create_button(f"{category.emoji} {category.name}", category.id) for category in categories]

    rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]

    rows.append([InlineKeyboardButton(text=_("💾 Saqlash"), callback_data="save")])

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return keyboard_markup
