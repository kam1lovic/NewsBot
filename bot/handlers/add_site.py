from urllib.parse import urlparse

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.buttons.keyboard import add_site_or_category
from bot.states import AddSiteState, Profile
from database.base import db
from database.models import User, Site

add_site_router = Router()


def is_valid_url(url: str) -> bool:
    """URL validligini tekshirish uchun funksiyamiz."""
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


@add_site_router.message(AddSiteState.waiting_for_site_url)
async def receive_site_url(message: Message, state: FSMContext):
    url = message.text.strip()

    # URL formatini tekshirish
    if not is_valid_url(url):
        await message.answer(_("Iltimos, URL ni http:// yoki https:// bilan boshlanadigan formatda yuboring."))
        return

    user_id = message.from_user.id
    user = await db.get(User, user_id)

    # Saytning mavjudligini tekshirish
    site = await Site.get_site_by_url(url)

    if site:
        site_id = site.id

        # Foydalanuvchining allaqachon bog'langan saytlarini olish
        user_sites = await user.get_sites()
        if site_id in [us.id for us in user_sites]:
            await message.answer(_("Ushbu sayt allaqachon sizga bog'langan 😊"))
        else:
            # Foydalanuvchi saytni bog'lash
            await user.add_user_sites([site_id])
            await message.answer(_("Ushbu sayt foydalanuvchiga bog'landi 🌐"))
    else:
        # Yangi sayt yaratish
        new_site = await Site.create(url=url)
        site_id = new_site.id
        await message.answer(_("Ushbu sayt yangi sayt sifatida saqlandi 😊✅"))

        # Foydalanuvchi saytni bog'lash
        await user.add_user_sites([site_id])
        await message.answer(_("Ushbu sayt foydalanuvchiga bog'landi 🌐"))

    # Holatni Profilga o'zgartirish va klaviaturani qaytarish
    await state.set_state(Profile.profile)
    btn = await add_site_or_category()
    await message.answer(_("Siz profil bo'limiga qaytdingiz. Iltimos, boshqa amalni tanlang."), reply_markup=btn)
