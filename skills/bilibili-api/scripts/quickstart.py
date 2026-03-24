#!/usr/bin/env python3
"""
bilibili-api Quickstart Example

Demonstrates basic video info retrieval using both async and sync patterns.

Usage:
    uv run python quickstart.py
    # or
    python quickstart.py
"""

import asyncio
from bilibili_api import video

from bilibili_api import sync  # noqa: F401 - used for sync_example


# Async version
async def async_example():

    print("=== Async Example ===")

    # Create video instance
    v = video.Video(bvid="BV1uv411q7Mv")

    # Get video info
    info = await v.get_info()

    print(f"Title: {info['title']}")
    print(f"BV ID: {info['bvid']}")
    print(f"Author: {info['owner']['name']}")
    print(f"Views: {info['stat']['view']:,}")
    print(f"Likes: {info['stat']['like']:,}")
    print(f"Description: {info['desc'][:100]}...")

    # Get online count
    online = await v.get_online()
    print(f"Online viewers: {online['total']}")

# Sync version
def sync_example():
    print("\n=== Sync Example ===")

    v = video.Video(bvid="BV1GK4y1V7HP")
    info = sync(v.get_info())

    print(f"Title: {info['title']}")
    print(f"Views: {info['stat']['view']:,}")

if __name__ == "__main__":
    # Run async example
    asyncio.run(async_example())

    # Run sync example
    sync_example()
