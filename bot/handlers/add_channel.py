from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from bot.buttons.keyboard import add_site_or_category
from bot.states import AddChannelState, Profile
from database.base import db
from database.models import Channel, User

add_channel_router = Router()
PROHIBITED_WORDS = []


@add_channel_router.message(AddChannelState.waiting_for_channel_name)
async def receive_channel_name(message: Message, state: FSMContext):
    channel_name = message.text.strip()

    if any(word in channel_name.lower() for word in PROHIBITED_WORDS):
        await message.answer(_("Bu kanal nomi nomaqbul so'zlarni o'z ichiga oladi. Iltimos, boshqa nom kiriting:"))
        return

    # Kanal nomini saqlash
    await state.update_data(channel_name=channel_name)
    await message.answer(_(f"Kanal nomi qabul qilindi ✅!"))
    await message.answer(_("Endi, kanal usernameni yuboring ‼️"))
    await state.set_state(AddChannelState.waiting_for_channel_username)


@add_channel_router.message(AddChannelState.waiting_for_channel_username)
async def receive_channel_username(message: Message, state: FSMContext):
    channel_username = message.text.strip()

    # Username formatini tekshirish
    if channel_username.startswith("t.me/") or channel_username.startswith("@"):
        await message.answer(
            _("Iltimos, username ni t.me/ yoki @ formatida emas, faqat username ni kiriting, Misol uchun ⤵️\n\n"
              "<i>t.me/kunuzofficial ❌ @kunuzofficial ❌ --> kunuzofficial ✅</i>"),
            disable_web_page_preview=True
        )
        return

    # Oldingi holatdagi kanallarni olish
    data = await state.get_data()
    channel_name = data.get('channel_name', None)

    # Kanal mavjudligini tekshirish
    existing_channel = await Channel.get_channels_by_username(username=channel_username)
    user_id = message.from_user.id
    user = await db.get(User, user_id)

    if existing_channel:
        channel = existing_channel[0]
        channel_id = channel.id

        # Foydalanuvchining mavjud kanallarini olish
        user_channels = await user.get_user_channels()
        if channel_id in [uc.id for uc in user_channels]:
            await message.answer(_("Ushbu kanal allaqachon sizga bog'langan 😊"))
        else:
            # Kanalni foydalanuvchiga bog'lash
            await user.add_user_channels([channel_id])
            await message.answer(_("Ushbu kanal foydalanuvchiga bog'landi 📣"))
    else:
        # Yangi kanal yaratish
        new_channel = await Channel.create(name=channel_name, username=channel_username)
        channel_id = new_channel.id
        await message.answer(_("Ushbu kanal yangi kanal sifatida saqlandi 😊✅"))

        # Kanalni foydalanuvchiga bog'lash
        await user.add_user_channels([channel_id])
        await message.answer(_("Ushbu kanal foydalanuvchiga bog'landi 📣"))

    # Holatni Profilga o'zgartirish va klaviaturani qaytarish
    await state.set_state(Profile.profile)
    btn = await add_site_or_category()
    await message.answer(_("Siz profil bo'limiga qaytdingiz. Iltimos, boshqa amalni tanlang."), reply_markup=btn)
