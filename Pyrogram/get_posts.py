#!/usr/bin/env python3

import asyncio
import json
import os
import sys

from Pyrogram.client import AGGREGATOR_CHANNEL

current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(current_dir)

sys.path.append(project_root)
import aiofiles

from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.errors import ChannelInvalid, ChannelPrivate, UsernameInvalid, UsernameNotOccupied, PeerIdInvalid
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from database.models import Post

from database.base import db

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
app = Client("get_posts", api_id=api_id, api_hash=api_hash)

LAST_POST_TIME_FILE = "last_post_time.json"


async def load_last_post_time():
    if os.path.exists(LAST_POST_TIME_FILE):
        async with aiofiles.open(LAST_POST_TIME_FILE, "r") as f:
            return json.loads(await f.read())
    return {}


async def save_last_post_time(last_post_time):
    async with aiofiles.open(LAST_POST_TIME_FILE, "w") as f:
        await f.write(json.dumps(last_post_time))


async def post_exists(post_link, session):
    result = await session.execute(select(Post).filter_by(post_link=post_link))
    return result.scalar() is not None


async def get_channel_posts(channel):
    data = []
    last_post_time = await load_last_post_time()

    async with app:
        print(f"Getting posts from {channel}...")
        last_id = last_post_time.get(channel)

        try:
            found_posts = False
            posts = []

            async for post in app.get_chat_history(channel):
                if last_id and post.id <= int(last_id):
                    break

                post_link = f"https://t.me/{channel}/{post.id}"
                content = (
                        post.text or
                        post.caption or
                        getattr(post, 'formatted_text', None) or
                        "Havola orqali ko'ring 🖇"
                )

                posts.append({"post_link": post_link, "content": content})
                found_posts = True

                if len(posts) >= 4:
                    break

            if found_posts:
                last_post_time[channel] = str(posts[0]["post_link"].split("/")[-1])
                await save_last_post_time(last_post_time)
                data.extend(posts)

        except (ChannelInvalid, ChannelPrivate, UsernameInvalid, UsernameNotOccupied, PeerIdInvalid) as e:
            print(f"Ushbu kanal username xato: '{channel}', Error: {e}")

    return data


async def main():
    channel_username = AGGREGATOR_CHANNEL
    data = await get_channel_posts(channel_username)
    print(data)

    for post_data in data:
        try:
            if await post_exists(post_data['post_link'], db):
                print(f"Post already exists: {post_data['post_link']}")
                continue
            new_post = Post(
                post_link=post_data['post_link'],
                content=post_data['content']
            )
            db.add(new_post)
            await db.commit()
            print(f"Post saved: {new_post.post_link}")
        except IntegrityError:
            await db.rollback()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
