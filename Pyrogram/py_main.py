import asyncio
from pyrogram.errors import (
    ChannelInvalid, ChannelPrivate, UsernameInvalid,
    UsernameNotOccupied, PeerIdInvalid, FloodWait
)
from client import app, send_posts_to_channel
from storage import load_last_post_ids, save_last_post_ids
from database.models import Channel


async def get_channel_posts(channels):
    data = []
    last_post_ids = await load_last_post_ids()
    async with app:
        for channel in channels:
            print(f"Getting posts from {channel}...")
            last_id = int(last_post_ids.get(channel, 0))
            try:
                posts = []
                async for post in app.get_chat_history(channel, limit=4):
                    if post.id <= last_id:
                        break
                    posts.append(post)

                if posts:
                    posts = posts[::-1]
                    media_seen = set()

                    for post in posts:
                        if post.pinned_message or post.service:
                            continue

                        post_link = f"https://t.me/{channel}/{post.id}"
                        content = (
                                post.text or post.caption or
                                getattr(post, 'formatted_text', None) or None
                        )

                        if not content:
                            continue

                        media = None
                        media_type = None

                        if post.media_group_id:
                            if post.media_group_id in media_seen:
                                continue
                            media_seen.add(post.media_group_id)

                        if post.photo:
                            media = post.photo.file_id
                            media_type = 'photo'
                        elif post.video:
                            media = post.video.file_id
                            media_type = 'video'

                        data.append({
                            "post_link": post_link,
                            "content": content,
                            "media": media,
                            "media_type": media_type
                        })

                    last_post_ids[channel] = posts[-1].id

            except (ChannelInvalid, ChannelPrivate, UsernameInvalid, UsernameNotOccupied, PeerIdInvalid) as e:
                print(f"Error with channel '{channel}': {e}")
                continue
            except FloodWait as e:
                print(f"Rate limit reached. Waiting for {e.value} seconds...")
                await asyncio.sleep(e.value)

            await asyncio.sleep(1)

    await save_last_post_ids(last_post_ids)
    return data


async def main():
    channels = await Channel.get_all()
    channel_usernames = [channel.username for channel in channels]
    data = await get_channel_posts(channel_usernames)
    print(f"{len(data)} new posts fetched.")

    if data:
        await send_posts_to_channel(data)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
