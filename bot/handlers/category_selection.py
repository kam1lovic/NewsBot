from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _

from bot.buttons.inline import category_buttons, organization_type
from bot.buttons.keyboard import add_site_or_category, select_web_or_channel
from bot.states import CategorySelection, Profile, Organizations
from bot.utils import process_urls
from database.base import db
from database.models import User

category_router = Router()


@category_router.message(StateFilter(CategorySelection.select_web_or_telegram))
async def get_selected_data(message: Message, state: FSMContext):
    if message.text == _("Saytlar 🌐"):
        await state.set_state(CategorySelection.web_selected)
        await message.answer(
            _("🌐 Siz veb saytlarni tanladingiz!\nSayt linklarini kiriting. Har birini alohida kiriting.\n\n🔗 <i>Misol uchun:</i> \nhttps://example.uz/"),
            reply_markup=ReplyKeyboardRemove())
    elif message.text == _("Telegram kanallar 📣"):
        await state.set_state(CategorySelection.telegram_selected)
        user = await User.get(message.from_user.id)
        user_language = user.language
        reply_buttons = await category_buttons(user_language)
        await message.answer(
            _("🔔 Siz Telegram kanallarini tanladingiz!\n\nKategoriya tanlang. Bir nechta kategoriya tanlab, ularni saqlashingiz mumkin!"),
            reply_markup=reply_buttons)
    elif message.text == _("Profil 👤"):
        await state.set_state(Profile.profile)
        button = await add_site_or_category()
        await message.answer(_("Profil bo'limi tanlandi!"), reply_markup=button)
    elif message.text == _("Davlat organlari bilan bo'glanish ☎️"):
        await state.set_state(Organizations.organ)
        user = await User.get(message.from_user.id)
        user_language = user.language
        button = await organization_type(user_language)
        await message.answer(_("Davlat organlari bilan bo'glanish tanlandi!"), reply_markup=button)
    else:
        await message.answer(_("❗️Iltimos, quyidagi tugmalardan birini tanlang."))


@category_router.callback_query(lambda c: c.data.startswith("category_"))
async def toggle_category(callback_query: CallbackQuery, state: FSMContext):
    category_id = int(callback_query.data.split("_")[1])

    data = await state.get_data()
    selected_categories = data.get("selected_categories", [])

    if category_id in selected_categories:
        selected_categories.remove(category_id)
    else:
        selected_categories.append(category_id)

    await state.update_data(selected_categories=selected_categories)
    user = await User.get(callback_query.from_user.id)
    user_language = user.language
    reply_markup = await category_buttons(user_language, selected_categories=selected_categories)
    await callback_query.message.edit_reply_markup(reply_markup=reply_markup)


@category_router.callback_query(lambda c: c.data == "save")
async def save_selected_categories(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_categories = data.get("selected_categories", [])
    user_id = callback_query.from_user.id

    if not selected_categories:
        await callback_query.answer(_("Iltimos, kamida bitta toifani tanlang."), show_alert=True)
        return

    user = await User.get(user_id)

    if user:
        user_categories = await user.get_categories()
        existing_category_ids = [category.id for category in user_categories]
        selected_categories = [
            cat_id for cat_id in selected_categories if cat_id not in existing_category_ids
        ]

        if selected_categories:
            await user.add_user_categories(category_ids=selected_categories)
    lang_code = data['locale']
    button = await select_web_or_channel(lang_code)
    await callback_query.answer(_("Kategoriyalar muvaffaqiyatli saqlandi ✅"), show_alert=True)
    await state.set_state(CategorySelection.select_web_or_telegram)
    await callback_query.message.answer(_("Kategoriyalar saqlandi va endi sizga muntazam yangiliklar yuboriladi 😊"),
                                        reply_markup=button)


@category_router.message(StateFilter(CategorySelection.web_selected))
async def get_sites_from_user(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    user = await db.get(User, user_id)
    lang_code = data['locale']
    button = await select_web_or_channel(lang_code)

    if message.text == "/done":
        site_ids = data.get('site_ids', [])

        if site_ids:
            await user.add_user_sites(site_ids)
            await message.answer(_("✅ Barcha saytlar saqlandi va sizga muntazam yangiliklar yuboriladi!"))
        else:
            await message.answer(_("❗️Hech qanday sayt saqlanmadi."))

        await state.set_state(CategorySelection.select_web_or_telegram)
        await message.answer(_("Siz bosh sahifaga qaytdingiz. Boshqa amal bajarishni hohlaysizmi?"),
                             reply_markup=button)
        return

    urls = message.text.strip().split()
    site_ids, already_saved_urls, invalid_urls = await process_urls(user_id, urls)

    if site_ids:
        data = await state.get_data()
        existing_site_ids = data.get('site_ids', [])
        updated_site_ids = existing_site_ids + site_ids

        await state.update_data(site_ids=updated_site_ids)
        count = len(site_ids)
        await message.answer(_("✅ Sayt(lar) muvaffaqiyatli saqlandi va hisobingizga qo'shildi."))

    if already_saved_urls:
        saved_urls = ', '.join(already_saved_urls)
        await message.answer(_("❗️Bu sayt(lar) allaqachon saqlangan"))

    if invalid_urls:
        invalid_urls_str = ', '.join(invalid_urls)
        await message.answer(
            _("❗️Sayt linki formati noto'g'ri \nIltimos, qayta yuboring."))

    await message.answer(_("⏳ Yana saytlarni yuboring yoki tugatish uchun /done ni bosing."))
