import os
from pyrogram import Client
from pyrogram.errors import FloodWait
from asyncio import sleep
from dotenv import load_dotenv
from utils import link_random_word

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
AGGREGATOR_CHANNEL = os.getenv("AGGREGATOR_CHANNEL")

app = Client("get_posts", api_id=api_id, api_hash=api_hash)


async def send_posts_to_channel(posts):
    async with app:
        for post in posts:
            try:
                content_with_link = link_random_word(post['content'], post['post_link'])

                if post.get('media'):
                    if post['media_type'] == 'photo':
                        await app.send_photo(
                            chat_id=AGGREGATOR_CHANNEL,
                            photo=post['media'],
                            caption=content_with_link

                        )
                    elif post['media_type'] == 'video':
                        await app.send_video(
                            chat_id=AGGREGATOR_CHANNEL,
                            video=post['media'],
                            caption=content_with_link
                        )
                else:
                    await app.send_message(
                        chat_id=AGGREGATOR_CHANNEL,
                        text=content_with_link,
                        disable_web_page_preview=True,
                    )

                print(f"Post sent: {post['post_link']} with a random word linked.")
                await sleep(1.5)
            except FloodWait as e:
                print(f"Flood wait for {e.value} seconds.")
                await sleep(e.value)
            except Exception as e:
                print(f"Failed to send post: {post['post_link']} - Error: {str(e)}")
