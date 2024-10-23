import os
import json
import aiofiles

LAST_POST_IDS_FILE = "last_post_ids.json"


async def load_last_post_ids():
    if os.path.exists(LAST_POST_IDS_FILE):
        async with aiofiles.open(LAST_POST_IDS_FILE, "r") as f:
            content = await f.read()
            if content:
                return json.loads(content)
    return {}


async def save_last_post_ids(last_post_ids):
    async with aiofiles.open(LAST_POST_IDS_FILE, "w") as f:
        await f.write(json.dumps(last_post_ids))
