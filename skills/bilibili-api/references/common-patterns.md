# Common Patterns

## Async/Await Pattern

All API methods are async. Use `asyncio.run()` for the main entry point:

```python
import asyncio
from bilibili_api import video, Credential

async def main():
    v = video.Video(bvid="BV1uv411q7Mv")
    info = await v.get_info()
    print(info["title"])

asyncio.run(main())
```

### Multiple Concurrent Requests

```python
import asyncio
from bilibili_api import video

async def fetch_multiple(bvids):
    tasks = [video.Video(bvid=bv).get_info() for bv in bvids]
    results = await asyncio.gather(*tasks)
    return results

asyncio.run(fetch_multiple(["BV1uv411q7Mv", "BV1GK4y1V7HP"]))
```

## Sync Wrapper

For scripts that don't need async:

```python
from bilibili_api import sync, video

v = video.Video(bvid="BV1uv411q7Mv")
info = sync(v.get_info())
print(info["title"])
```

**Limitations:**
- Cannot use `sync()` inside an already-running event loop
- For nested async calls, use `asyncio.run()` or proper async/await

```python
# WRONG - sync() inside async function
async def main():
    info = sync(v.get_info())  # RuntimeError!

# CORRECT
async def main():
    info = await v.get_info()
```

## Error Handling

### Exception Hierarchy

```
ApiException (base)
├── ArgsException           — Invalid arguments
├── NetworkException        — HTTP/network errors
├── ResponseException       — Response parsing errors
│   └── ResponseCodeException — API returned error code
├── LoginError              — Login failures
├── GeetestException        — Captcha errors
├── CookiesRefreshException — Cookie refresh failed
├── VideoUploadException    — Video upload errors
├── LiveException           — Live streaming errors
├── DanmakuClosedException  — Danmaku connection closed
├── WbiRetryTimesExceedException — WBI retries exhausted
├── DynamicExceedImagesException — Too many images in dynamic
├── ExClimbWuzhiException   — Anti-spider triggered
└── CredentialNo*Exception  — Missing credential fields
    ├── CredentialNoSessdataException
    ├── CredentialNoBiliJctException
    ├── CredentialNoBuvid3Exception
    ├── CredentialNoBuvid4Exception
    ├── CredentialNoDedeUserIDException
    └── CredentialNoAcTimeValueException
```

### Handling API Errors

```python
from bilibili_api import video, ResponseCodeException, NetworkException

async def safe_get_info(bvid):
    v = video.Video(bvid=bvid)
    try:
        info = await v.get_info()
        return info
    except ResponseCodeException as e:
        # Bilibili API returned error
        print(f"API error {e.code}: {e.msg}")
        # Common codes:
        # -400: Request error
        # -403: Access denied
        # -404: Not found
        # -509: Rate limited
        return None
    except NetworkException as e:
        # HTTP/network failure
        print(f"Network error {e.status}: {e.msg}")
        return None
```

### Credential Validation

```python
from bilibili_api import Credential, CredentialNoSessdataException

async def require_auth(credential):
    if not credential.has_sessdata():
        raise CredentialNoSessdataException()
    # or use the built-in method
    credential.raise_for_no_sessdata()
```

## Event System (AsyncEvent)

Used by `LiveDanmaku`, `VideoOnlineMonitor`, and uploaders for event-driven callbacks.

### Basic Usage

```python
from bilibili_api import live

room = live.LiveDanmaku(room_display_id=123456)

@room.on("DANMU_MSG")
async def on_danmaku(event):
    # event["data"] contains the raw message
    content = event["data"]["info"][1]  # danmaku text
    user = event["data"]["info"][2][1]  # username
    print(f"{user}: {content}")

await room.connect()
```

### Multiple Events

```python
@room.on("DANMU_MSG")
async def on_danmaku(event):
    print(f"Danmaku: {event}")

@room.on("SEND_GIFT")
async def on_gift(event):
    print(f"Gift: {event}")

@room.on("SUPER_CHAT_MESSAGE")
async def on_superchat(event):
    print(f"Super Chat: {event}")
```

### Catch All Events

```python
@room.on("__ALL__")
async def on_all(event):
    print(f"Event: {event}")
```

### Programmatic Listener Management

```python
# Add listener
def handler(event):
    print(event)

room.add_event_listener("DANMU_MSG", handler)

# Remove listener
room.remove_event_listener("DANMU_MSG", handler)
```

## Danmaku

### Sending Danmaku

```python
from bilibili_api import video, Danmaku, DmMode, DmFontSize, Credential

async def send_danmaku():
    cred = Credential(sessdata="...", bili_jct="...")
    v = video.Video(bvid="BVxxxxxxxx", credential=cred)

    dm = Danmaku(
        text="Hello from bilibili-api!",
        dm_time=5.0,           # Time in video (seconds)
        mode=DmMode.FLY,       # Scroll mode
        font_size=DmFontSize.NORMAL,  # Font size
        color=0xFFFFFF,        # White (hex)
    )

    await v.send_danmaku(dm)
```

### Danmaku Enums

```python
from bilibili_api import DmMode, DmFontSize

# DmMode
DmMode.FLY      # 1 - Scroll
DmMode.TOP      # 2 - Top fixed
DmMode.BOTTOM   # 3 - Bottom fixed
DmMode.REVERSE  # 4 - Reverse scroll

# DmFontSize
DmFontSize.SMALL   # 18px
DmFontSize.NORMAL  # 25px
DmFontSize.BIG     # 36px
```

### Getting Danmaku

```python
async def get_danmaku():
    v = video.Video(bvid="BVxxxxxxxx")
    danmakus = await v.get_danmakus(page_index=0)
    for dm in danmakus:
        print(f"{dm.dm_time}s: {dm.text}")
```

## Video Download Pattern

```python
import asyncio
from bilibili_api import video, get_client, HEADERS

async def download_video(bvid, output="video.mp4"):
    v = video.Video(bvid=bvid)

    # Get download URLs
    urls = await v.get_download_url(page_index=0)

    # Use VideoDownloadURLDataDetecter to parse
    from bilibili_api import video
    detecter = video.VideoDownloadURLDataDetecter(urls)

    # Detect best streams
    streams = detecter.detect_best_streams()
    video_url = streams[0].url  # Video stream
    audio_url = streams[1].url  # Audio stream (may be None for some videos)

    # Download using client
    client = get_client()

    # Download video
    dwn_id = await client.download_create(video_url, HEADERS)
    total = client.download_content_length(dwn_id)

    with open(output, "wb") as f:
        downloaded = 0
        while True:
            chunk = await client.download_chunk(dwn_id)
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            print(f"Downloaded: {downloaded}/{total} bytes", end="\r")

    print(f"\nSaved to {output}")

# For dash videos (separate video/audio), use ffmpeg to merge:
# ffmpeg -i video.mp4 -i audio.m4a -c copy output.mp4
```

## ID Conversion

```python
from bilibili_api import aid2bvid, bvid2aid

# AV to BV
bvid = aid2bvid(170001)        # "BV17x411w7KC"

# BV to AV
aid = bvid2aid("BV17x411w7KC") # 170001
```

## Link Utilities

### Parse Any Bilibili Link

```python
from bilibili_api import parse_link, ResourceType

async def parse(url):
    result = await parse_link(url)
    print(result.resource_type)  # ResourceType enum
    print(result.id)             # Resource ID
    print(result.obj)            # Corresponding object instance
```

### Resolve Short URLs

```python
from bilibili_api import get_real_url

async def resolve():
    real_url = await get_real_url("https://b23.tv/BV1uv411q7Mv")
    print(real_url)  # Full bilibili URL
```

## Picture Class

```python
from bilibili_api import Picture

# From file
pic = Picture.from_file("./image.png")

# From URL
pic = await Picture.from_url("https://example.com/image.png")

# From content
pic = Picture.from_content(content_bytes, format="png")

# Convert format
pic_jpg = pic.convert_format("jpeg")

# Use in dynamic, comment, etc.
```

## Pagination Pattern

Many APIs return paginated results. Use `pn` (page number) or `offset`:

```python
from bilibili_api import user

async def get_all_videos(uid):
    u = user.User(uid=uid)
    page = 1
    all_videos = []

    while True:
        result = await u.get_videos(pn=page, ps=30)
        videos = result["list"]["vlist"]
        if not videos:
            break
        all_videos.extend(videos)
        page += 1

        # Stop if we've seen all videos
        if len(all_videos) >= result["page"]["count"]:
            break

    return all_videos
```

### Offset-Based (Dynamics)

```python
async def get_dynamics(uid):
    u = user.User(uid=uid)
    offset = None
    all_dynamics = []

    for _ in range(5):  # Get 5 pages
        result = await u.get_dynamics_new(offset=offset)
        if not result:
            break
        all_dynamics.extend(result["items"])
        offset = result.get("offset")
        if not offset:
            break

    return all_dynamics
```
