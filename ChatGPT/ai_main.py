import asyncio
from sqlalchemy import select
from database import db
from database.models import Category, Post
from ChatGPT.save_posts import save_summarized_posts


async def main():
    try:
        category_result = await db.execute(select(Category))
        categories = [category.name for category in category_result.scalars().all()]

        post_result = await db.execute(select(Post))
        news = [f"{post.content} {post.post_link}" for post in post_result.scalars().all()]

        await save_summarized_posts(news, categories)
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        await db.rollback()
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())
