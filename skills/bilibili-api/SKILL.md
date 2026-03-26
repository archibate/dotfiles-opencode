---
name: bilibili-api
description: This skill should be used when the user asks to "use bilibili API", "download bilibili video", "get bilibili user info", "list bilibili favorites", "send bilibili danmaku", "upload video to bilibili", "monitor bilibili live room", "search bilibili", "get bilibili comments", or needs guidance on the bilibili_api Python library usage, authentication, API endpoints, or workflow patterns.
version: 0.1.0
---

# bilibili-api Skill

## Overview

`bilibili-api` (package: `bilibili-api-python`, v17.4.1) is a comprehensive async Python wrapper for Bilibili's APIs with 400+ endpoints across 42 modules. All operations are async (asyncio-based) with a sync wrapper available. Supports three HTTP backends: curl_cffi, aiohttp, httpx.

- **Source code:** `<project_root>/bilibili_api/`
- **Documentation (Chinese):** `references/docs/`
- **Module API docs:** `references/docs/modules/*.md`
- **Usage examples:** `references/docs/examples/*.md`

## Quick Start

Install the library and at least one HTTP backend:

```bash
uv pip install bilibili-api-python aiohttp
# or: uv pip install bilibili-api-python curl_cffi
# or: uv pip install bilibili-api-python httpx
```

Minimal example (anonymous, no credentials needed):

```python
import asyncio
from bilibili_api import video

async def main():
    v = video.Video(bvid="BV1uv411q7Mv")
    info = await v.get_info()
    print(info["title"], info["stat"]["view"])

asyncio.run(main())
```

Or use the sync wrapper:

```python
from bilibili_api import video, sync

v = video.Video(bvid="BV1uv411q7Mv")
info = sync(v.get_info())
print(info["title"])
```

See `scripts/quickstart.py` for a runnable example.

## Credential Setup

Most read operations work without credentials. Write operations (like, comment, upload) and some read operations (user history, favorites) require authentication via the `Credential` class.

```python
from bilibili_api import Credential

credential = Credential(
    sessdata="...",       # Required for GET (read) operations
    bili_jct="...",       # Required for POST (write) operations
    buvid3="...",         # Device ID (auto-generated if omitted)
    buvid4="...",         # Device ID v4 (optional)
    dedeuserid="...",     # User ID (rarely needed)
    ac_time_value="...",  # For cookie refresh only
)
```

**Extract from browser:** Open bilibili.com > F12 DevTools > Application (Chrome) or Storage (Firefox) > Cookies > `.bilibili.com` > copy `SESSDATA`, `bili_jct`, `buvid3`.

**Programmatic login:** Use `login_v2` module for QR code, password, or SMS login.

**Cookie refresh:** Use `credential.check_refresh()` and `credential.refresh()` when cookies expire.

For complete details, consult **`references/credential-setup.md`**. To validate credentials, run `scripts/credential_check.py`.

## Key Modules

| Category | Module | Description | Key Class |
|----------|--------|-------------|-----------|
| **Content** | `video` | Video info, actions, danmaku, download | `Video` |
| | `bangumi` | Anime/drama series | `Bangumi` |
| | `article` | Column articles | `Article` |
| | `audio` | Audio tracks | `Audio` |
| | `manga` | Manga/comics | `Manga` |
| | `cheese` | Paid courses | `CheeseList`, `CheeseVideo` |
| | `opus` | Image posts | `Opus` |
| | `note` | Notes | `Note` |
| **Social** | `user` | User profiles, followers, videos | `User` |
| | `dynamic` | User dynamics/feeds | `Dynamic` |
| | `comment` | Comments on any resource | `Comment` |
| | `session` | Private messages | (functions) |
| | `emoji` | Emoji/sticker packs | (functions) |
| **Discovery** | `search` | Search videos/users/articles | (functions) |
| | `hot` | Trending content | (functions) |
| | `rank` | Rankings | (functions) |
| | `homepage` | Homepage recommendations | (functions) |
| | `video_zone` | Video category zones | (functions) |
| **Live** | `live` | Live rooms, danmaku, gifts | `LiveRoom`, `LiveDanmaku` |
| | `live_area` | Live streaming categories | (functions) |
| **Upload** | `video_uploader` | Video upload workflow | `VideoUploader` |
| | `audio_uploader` | Audio upload workflow | `AudioUploader` |
| **Account** | `login_v2` | Login (QR/password/SMS) | `QrCodeLogin` |
| | `creative_center` | Creator dashboard | (functions) |
| | `favorite_list` | Favorites management | `FavoriteList` |

For the complete list of all 42 modules with classes and methods, consult **`references/api-modules.md`**.

## Core Patterns

### Async Usage

All API methods are async. Standard pattern:

```python
import asyncio
from bilibili_api import video, Credential

async def main():
    cred = Credential(sessdata="...", bili_jct="...")
    v = video.Video(bvid="BVxxxxxxxx", credential=cred)
    info = await v.get_info()
    await v.like(True)

asyncio.run(main())
```

### Sync Wrapper

For scripts that don't need async:

```python
from bilibili_api import sync
result = sync(v.get_info())
```

Note: `sync()` cannot be called inside an already-running event loop.

### Error Handling

```python
from bilibili_api import ResponseCodeException, NetworkException

try:
    info = await v.get_info()
except ResponseCodeException as e:
    print(f"API error {e.code}: {e.msg}")  # Bilibili API returned error
except NetworkException as e:
    print(f"HTTP error {e.status}: {e.msg}")  # Network/HTTP failure
```

Key exceptions: `ResponseCodeException` (API error code), `NetworkException` (HTTP error), `ArgsException` (bad parameters), `CredentialNo*Exception` (missing auth fields).

### Event System (WebSocket)

Used by `LiveDanmaku`, `VideoOnlineMonitor`, uploaders:

```python
from bilibili_api import live

room = live.LiveDanmaku(room_display_id=123456)

@room.on("DANMU_MSG")
async def on_danmaku(event):
    print(event["data"]["info"][1])  # danmaku text

await room.connect()
```

### ID Conversion

```python
from bilibili_api import aid2bvid, bvid2aid
bvid = aid2bvid(170001)        # -> "BV17x411w7KC"
aid = bvid2aid("BV17x411w7KC") # -> 170001
```

### Link Parsing

```python
from bilibili_api import parse_link, get_real_url
# Resolve b23.tv short URLs
real_url = await get_real_url("https://b23.tv/xxxxxxx")
# Parse any bilibili link to resource type + ID
resource = await parse_link(real_url)
```

For detailed patterns (download, danmaku, pagination, Picture class), consult **`references/common-patterns.md`**.

## Configuration

```python
from bilibili_api import request_settings, request_log, select_client

# Proxy
request_settings.set_proxy("http://127.0.0.1:7890")

# Timeout (default: 30s)
request_settings.set_timeout(60.0)

# Switch HTTP backend
select_client("curl_cffi")  # or "aiohttp", "httpx"

# Enable request logging
request_log.set_on(True)

# Anti-spider (usually automatic)
from bilibili_api import recalculate_wbi, refresh_buvid
await recalculate_wbi()  # Force WBI key refresh
await refresh_buvid()    # Force buvid refresh
```

For full configuration details, consult **`references/configuration.md`**.

## Reference Files

### Detailed References

| File | Description |
|------|-------------|
| **`references/credential-setup.md`** | Complete credential guide: browser extraction, programmatic login (QR/password/SMS), cookie refresh |
| **`references/api-modules.md`** | All 42 modules with classes, key methods, and auth requirements |
| **`references/configuration.md`** | Request settings, proxy, HTTP clients, logging, anti-spider measures |
| **`references/common-patterns.md`** | Async/sync patterns, error handling, events, danmaku, download, pagination |
| **`references/video-guide.md`** | Video module deep dive: info, actions, danmaku, download with quality selection |
| **`references/user-guide.md`** | User module deep dive: profile, content listing, social actions, pagination |
| **`references/live-guide.md`** | Live module deep dive: room info, WebSocket danmaku, gift tracking |
| **`references/upload-guide.md`** | Video/audio upload workflows with event monitoring |
| **`references/self-update.md`** | Skill self-update workflow: check for new releases, sync docs, update version info |

### Utility Scripts

| File | Description |
|------|-------------|
| **`scripts/quickstart.py`** | Minimal runnable example (anonymous video info retrieval) |
| **`scripts/credential_check.py`** | Validate credentials from environment variables |

### Source Documentation

For exhaustive API signatures, consult the project's built-in docs:
- **Module API reference:** `references/docs/modules/<module>.md`
- **Usage examples:** `references/docs/examples/<module>.md`
