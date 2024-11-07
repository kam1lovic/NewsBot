import asyncio
import random
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import db
from database.models import User, SummarizedPost
from main import bot

MAX_MESSAGE_LENGTH = 4096


async def get_all_users():
    result = await db.execute(
        select(User).options(selectinload(User.categories))
    )
    users = result.scalars().all()
    return users


async def get_unsent_summarized_posts(user):
    user_category_ids = [category.id for category in user.categories]

    if not user_category_ids:
        return []

    eight_hours_ago = datetime.utcnow() - timedelta(hours=8)

    result = await db.execute(
        select(SummarizedPost)
        .where(
            SummarizedPost.sent.is_(False),
            SummarizedPost.category_id.in_(user_category_ids),
            SummarizedPost.created_at >= eight_hours_ago
        )
    )
    posts = result.scalars().all()
    return posts


async def send_text_with_random_links(posts, user):
    messages = []
    current_message = ""

    def get_content_by_language(post, language):
        if language == 'en':
            return post.content_en
        elif language == 'ru':
            return post.content_ru
        else:
            return post.content_uz

    def get_category_name_by_language(category, language):
        if language == 'en':
            return category.name
        elif language == 'ru':
            return category.name_ru
        else:
            return category.name_uz

    posts_by_category = {}
    for post in posts:
        category = post.category
        if category not in posts_by_category:
            posts_by_category[category] = []
        posts_by_category[category].append(post)

    for category, category_posts in posts_by_category.items():
        # Foydalanuvchi tiliga mos ravishda kategoriya nomini olish
        category_name = get_category_name_by_language(category, user.language)
        category_header = f"<b>{category.emoji} {category_name.upper()}\n\n</b>"

        if len(current_message) + len(category_header) <= MAX_MESSAGE_LENGTH:
            current_message += category_header
        else:
            messages.append(current_message)
            current_message = category_header

        for post in category_posts:
            content = get_content_by_language(post, user.language)

            if not content:
                continue

            words = content.split()
            if not words:
                continue

            random_index = random.randrange(len(words))
            random_word = words[random_index]
            linked_word = f'<a href="{post.post_link}">{random_word}</a>'
            words[random_index] = linked_word

            modified_text = ' '.join(words)
            line = f"- {modified_text}.\n"

            if len(current_message) + len(line) <= MAX_MESSAGE_LENGTH:
                current_message += line
            else:
                messages.append(current_message)
                current_message = line

        current_message += "\n"

    if current_message:
        messages.append(current_message)

    for message in messages:
        await bot.send_message(
            user.id,
            message,
            parse_mode='HTML',
            disable_web_page_preview=True
        )


async def main():
    users = await get_all_users()

    if not users:
        print("No users found.")
        return

    for user in users:
        unsent_posts = await get_unsent_summarized_posts(user)

        if not unsent_posts:
            print(f"No unsent posts found for user {user.id}.")
            continue

        await send_text_with_random_links(unsent_posts, user)

        for post in unsent_posts:
            post.sent = True
            db.add(post)

    await db.commit()

    await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
