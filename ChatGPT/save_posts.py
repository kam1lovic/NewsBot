import json

from sqlalchemy import select

from ChatGPT.ai import generate_title
from database import db
from database.models import Category, SummarizedPost


async def save_summarized_posts(news: list, categories: list):
    generated_data = generate_title(news, categories)

    try:
        generated_dict = json.loads(generated_data)
        print(generated_dict, '\n---------------------------------------------------------------------')
    except json.JSONDecodeError:
        print("The result is not in JSON format.")
        return

    for result in generated_dict:
        if not isinstance(result, dict):
            print(f"Skipping invalid result: {result}")
            continue

        category_name = result.get('category')
        summary = result.get('title')
        post_link = result.get('post_link')

        if not category_name or not summary or not post_link:
            print(f"Missing category, summary, or post link in result: {result}")
            continue

        existing_post_result = await db.execute(
            select(SummarizedPost).filter_by(post_link=post_link)
        )
        existing_post = existing_post_result.scalars().first()

        if existing_post:
            print(f"Post with post_link '{post_link}' already exists. Skipping.")
            continue

        category_result = await db.execute(
            select(Category).filter_by(name=category_name)
        )
        category = category_result.scalars().first()

        if not category:
            print(f"Category '{category_name}' not found in the database. Skipping.")
            continue

        summarized_post = SummarizedPost(
            content_en=summary.get('en').strip(),
            content_uz=summary.get('uz').strip(),
            content_ru=summary.get('ru').strip(),
            category_id=category.id,
            post_link=post_link,
        )

        db.add(summarized_post)
        await db.commit()

        print(f"Summarized post saved: {summarized_post}")
