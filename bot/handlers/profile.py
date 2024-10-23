from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _

from bot.buttons.keyboard import select_web_or_channel
from bot.states import Profile, AddCategoryState, AddSiteState, AddChannelState, CategorySelection

profile_router = Router()


@profile_router.message(Profile.profile)
async def profile(message: Message, state: FSMContext):
    data = await state.get_data()
    lang_code = data["locale"]
    btn = await select_web_or_channel(lang_code)

    if message.text == _("Kategoriya qo'shish 🏷"):
        await message.answer(_("Iltimos, kategoriya nomini yuboring: "), reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddCategoryState.waiting_for_category_name)

    elif message.text == _("Sayt qo'shish 🌐"):
        await message.answer(_("🌐 Iltimos, sayt linklarini quyidagi formatda yuboring:\n\nhttps://example.com/"),
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddSiteState.waiting_for_site_url)

    elif message.text == _("Telegram kanal qo'shish 📣"):

        await message.answer(_("📣 Iltimos, kanal nomini yuboring:"), reply_markup=ReplyKeyboardRemove())

        await state.set_state(AddChannelState.waiting_for_channel_name)

    elif message.text == _("Orqaga  ⤵️"):
        await state.set_state(CategorySelection.select_web_or_telegram)
        await message.answer(_("Siz orqaga qaytdingiz ⤵️"), reply_markup=btn)

    else:

        await message.answer(_("Iltimos, tugmalardan birini tanlang‼️"))
