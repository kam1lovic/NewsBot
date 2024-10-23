import logging
import re

from aiogram.utils.i18n import gettext as _
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from database.base import db
from database.models import Site, user_sites, Category, Channel


async def save_categories_to_db():
    categories = [
        {"name": "Sport", "emoji": "⚽️"},
        {"name": "Technique", "emoji": "💻"},
        {"name": "Business", "emoji": "💼"},
        {"name": "Art", "emoji": "🎨"},
        {"name": "Health", "emoji": "🩺"},
        {"name": "Culture", "emoji": "🏛"},
        {"name": "Finance", "emoji": "💵"},
        {"name": "Science", "emoji": "🔬"},
        {"name": "Travel", "emoji": "✈️"},
        {"name": "Auto", "emoji": "🚗"},
        {"name": "Food", "emoji": "🍽"},
        {"name": "Fashion", "emoji": "👗"},
        {"name": "Games", "emoji": "🎮"},
        {"name": "Education", "emoji": "📚"},
        {"name": "Music", "emoji": "🎶"},
        {"name": "Nature", "emoji": "🌿"},
        {"name": "Movies", "emoji": "🎬"},
        {"name": "Sports_techniques", "emoji": "🤾‍"},
        {"name": "Family", "emoji": "👨‍👩‍👧‍👦"},
        {"name": "Art_history", "emoji": "🖼"},
        {"name": "Genetics", "emoji": "🧬"},
        {"name": "Energy", "emoji": "⚡️"},
        {"name": "Programming", "emoji": "💻"},
        {"name": "Scientific_techniques", "emoji": "🔧"},
        {"name": "Photography", "emoji": "📸"},
        {"name": "Animation", "emoji": "🎥"}
    ]

    existing_categories_query = select(Category.name)
    existing_categories_result = await db.execute(existing_categories_query)

    existing_categories = {row for row in existing_categories_result.scalars().all()}

    new_categories = [category for category in categories if category['name'] not in existing_categories]

    if new_categories:
        try:
            stmt = insert(Category).values(new_categories)
            await db.execute(stmt)
            await db.commit()
            print(f"Added {len(new_categories)} new categories to the database.")
        except IntegrityError as e:
            print(f"Error occurred while inserting categories: {e}")
    else:
        print("No new categories to add. All categories already exist.")


async def save_telegram_channels_to_db():
    channels = [
        {"name": "SPORT", "username": "uzsport_tv"},
        {"name": "YANGILIKLAR", "username": "Sara_Xabarlar"},
        {"name": "KUNUZ", "username": "kunuzofficial"},
        {"name": "DARYOUZ", "username": "Daryo"},
        {"name": "QORAXABARLAR", "username": "Qoraxabar"},
    ]

    existing_channels_query = select(Channel.username)
    existing_channels_result = await db.execute(existing_channels_query)

    existing_usernames = {row for row in existing_channels_result.scalars().all()}

    new_channels = [channel for channel in channels if channel['username'] not in existing_usernames]

    if new_channels:
        try:
            # Insert the new channels into the database
            stmt = insert(Channel).values(new_channels)
            await db.execute(stmt)
            await db.commit()
            print(f"Added {len(new_channels)} new Telegram channels to the database.")
        except IntegrityError as e:
            print(f"Error occurred while inserting Telegram channels: {e}")
    else:
        print("No new channels to add. All channels already exist.")


async def add_category(name: str, emoji: str, user_id: int):
    existing_category_query = select(Category).where(Category.name == name)
    existing_category_result = await db.execute(existing_category_query)
    existing_category = existing_category_result.scalar()

    if existing_category:
        msg = _("❗Ushbu kategoriya allaqachon mavjud.")
        return msg

    try:
        # Insert into Category with user_id
        stmt = insert(Category).values(name=name, emoji=emoji, user_id=user_id).returning(Category.id)
        result = await db.execute(stmt)
        category_id = result.scalar()

        await db.commit()

        msg = _("✅ Ushbu kategoriya muvaffaqqiyatli saqlandi ✅!")
        return msg

    except IntegrityError as e:
        await db.rollback()
        # Log the error for debugging
        logging.error(f"IntegrityError while adding category: {e}")
        msg = _("Kategoriya qo'shishga urinishda xatolik yuz berdi.")
        return msg
    except Exception as e:
        await db.rollback()
        # Log unexpected errors
        logging.error(f"Unexpected error while adding category: {e}")
        msg = _("Kategoriya qo'shishda xatolik yuz berdi.")
        return msg


async def process_urls(user_id, urls):
    valid_urls = []
    invalid_urls = []
    already_saved_urls = []
    site_ids = []

    for url in urls:
        if not re.match(r'^https?://', url):
            invalid_urls.append(url)
            continue

        site = (await db.execute(select(Site).where(Site.url == url))).scalar()

        if not site:
            try:
                result = await db.execute(insert(Site).values(url=url).returning(Site.id))
                site_id = result.scalar()
            except IntegrityError:
                invalid_urls.append(url)
                continue
        else:
            site_id = site.id

        user_site_exists = await db.execute(
            select(user_sites).where(user_sites.c.user_id == user_id, user_sites.c.site_id == site_id)
        )

        if user_site_exists.fetchone():
            already_saved_urls.append(url)
        else:
            site_ids.append(site_id)

    return site_ids, already_saved_urls, invalid_urls
