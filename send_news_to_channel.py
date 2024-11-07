import asyncio
import random
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import db
from database.models import SummarizedPost
from main import bot

MAX_MESSAGE_LENGTH = 4096
CHANNEL_USERNAME = '@vijimki_newsbot'


async def get_all_unsent_summarized_posts():
    eight_hours_ago = datetime.utcnow() - timedelta(hours=8)

    async with db._session as session:
        result = await session.execute(
            select(SummarizedPost)
            .options(selectinload(SummarizedPost.category))
            .where(
                SummarizedPost.sent_channel.is_(False),
                SummarizedPost.created_at >= eight_hours_ago
            )
            .order_by(SummarizedPost.category_id)
        )
        posts = result.scalars().all()
        return posts


async def send_posts_to_channel(posts):
    messages = []
    current_message = ""

    current_message += "<b>8 soatlik umumlashtirilgan habarlar</b>\n\n"

    posts_by_category = {}
    for post in posts:
        category = post.category
        if category not in posts_by_category:
            posts_by_category[category] = []
        posts_by_category[category].append(post)

    for category, category_posts in posts_by_category.items():
        category_header = f"<b>{category.emoji} {category.name_uz.upper()}\n</b>"
        if len(current_message) + len(category_header) <= MAX_MESSAGE_LENGTH:
            current_message += category_header
        else:
            messages.append(current_message)
            current_message = category_header

        for post in category_posts:
            content = post.content_uz
            if not content:
                continue

            words = content.split()
            if words:
                random_index = random.randint(0, len(words) - 1)
                random_word = words[random_index]
                linked_word = f'<a href="{post.post_link}">{random_word}</a>'
                words[random_index] = linked_word

            modified_text = ' '.join(words)
            line = f"- {modified_text}\n"

            if len(current_message) + len(line) <= MAX_MESSAGE_LENGTH:
                current_message += line
            else:
                messages.append(current_message)
                current_message = line

        current_message += "\n"

    current_message += "<i>Malumotlar OpenAI GPT-4 yordamida avtomatik ravishda yaratilgan. Ma'lumotlarning to'g'riligi tasdiqlanmagan.\n</i>"

    if current_message:
        messages.append(current_message)

    for message in messages:
        await bot.send_message(
            CHANNEL_USERNAME,
            message,
            parse_mode='HTML',
            disable_web_page_preview=True
        )


async def main():
    unsent_posts = await get_all_unsent_summarized_posts()

    if not unsent_posts:
        print("No unsent posts found.")
        return

    await send_posts_to_channel(unsent_posts)

    async with db._session as session:
        for post in unsent_posts:
            post.sent_channel = True
            session.add(post)

        await session.commit()

    await bot.session.close()


if __name__ == '__main__':
    db.init()
    asyncio.run(main())
