from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _


async def select_web_or_channel(lang_code):
    web_text = _("Saytlar 🌐", locale=lang_code)
    channel_text = _("Telegram kanallar 📣", locale=lang_code)
    profile_text = _("Profil 👤", locale=lang_code)
    organization_text = _("Davlat organlari bilan bo'glanish ☎️", locale=lang_code)

    web = KeyboardButton(text=web_text)
    channel = KeyboardButton(text=channel_text)
    profile = KeyboardButton(text=profile_text)
    contact_government_organizations = KeyboardButton(text=organization_text)

    design = [
        [channel, profile],
        [contact_government_organizations]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True, one_time_keyboard=True)


def get_language_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O'zbek"), KeyboardButton(text="🇬🇧 English")],
            [KeyboardButton(text="🇷🇺 Русский")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


async def add_site_or_category():
    category_text = _("Kategoriya qo'shish 🏷")
    # site_text = _("Sayt qo'shish 🌐")
    channel_text = _("Telegram kanal qo'shish 📣")
    back_text = _("Orqaga  ⤵️")

    category = KeyboardButton(text=category_text)
    # site = KeyboardButton(text=site_text)
    channel = KeyboardButton(text=channel_text)
    back = KeyboardButton(text=back_text)

    design = [
        [category, channel],
        [back]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True, one_time_keyboard=True)
