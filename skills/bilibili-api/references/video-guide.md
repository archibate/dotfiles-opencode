# Video Module Guide

## Video Class

```python
from bilibili_api import video, Credential

# By BV ID
v = video.Video(bvid="BV1uv411q7Mv")

# By AV ID
v = video.Video(aid=170001)

# With credentials (for actions)
cred = Credential(sessdata="...", bili_jct="...")
v = video.Video(bvid="BVxxxxxxxx", credential=cred)
```

## Information Methods

| Method | Description | Auth |
|--------|-------------|------|
| `get_info()` | Basic video info (title, stat, etc.) | No |
| `get_detail()` | Detailed info with related videos | No |
| `get_stat()` | View/like/coin/fav counts | No |
| `get_pages()` | Multi-part video pages | No |
| `get_online()` | Real-time viewer count | No |
| `get_tags()` | Video tags | No |
| `get_ai_conclusion()` | AI-generated summary | No |
| `get_subtitle()` | Subtitle data | No |
| `get_pbp()` | Playback progress data | No |

```python
async def get_video_info():
    v = video.Video(bvid="BV1uv411q7Mv")
    info = await v.get_info()
    print(f"Title: {info['title']}")
    print(f"Views: {info['stat']['view']}")
    print(f"Likes: {info['stat']['like']}")
```

## Action Methods (Require Credential)

| Method | Description |
|--------|-------------|
| `like(status)` | Like/unlike video |
| `pay_coin(num, like)` | Coin video (1-2 coins, like option) |
| `set_favorite(add_ids, del_ids)` | Add/remove from favorites |
| `triple()` | Like, coin, and favorite at once |
| `share()` | Record a share action |

```python
async def interact_with_video():
    cred = Credential(sessdata="...", bili_jct="...")
    v = video.Video(bvid="BVxxxxxxxx", credential=cred)

    # Like
    await v.like(True)

    # Coin + like
    await v.pay_coin(num=1, like=True)

    # Triple (like + coin + fav)
    await v.triple()

    # Add to favorites
    await v.set_favorite(add_ids=[123456])  # favorite_list ID
```

## Danmaku Methods

| Method | Description |
|--------|-------------|
| `get_danmakus(page_index)` | Get danmaku list |
| `get_danmaku_xml(page_index)` | Get raw XML danmaku |
| `get_special_dms(page_index)` | Get special danmaku |
| `send_danmaku(danmaku)` | Send danmaku (requires auth) |
| `get_history_danmaku_index(date)` | Get historical danmaku index |

```python
from bilibili_api import Danmaku, DmMode, DmFontSize

async def send_danmaku():
    cred = Credential(sessdata="...", bili_jct="...")
    v = video.Video(bvid="BVxxxxxxxx", credential=cred)

    dm = Danmaku(
        text="Hello!",
        dm_time=5.0,              # Video time (seconds)
        mode=DmMode.FLY,          # Scroll mode
        font_size=DmFontSize.NORMAL,
        color=0xFFFFFF,           # White
    )
    await v.send_danmaku(dm)

async def get_danmaku():
    v = video.Video(bvid="BV1AV411x7Gs")
    danmakus = await v.get_danmakus(page_index=0)
    for dm in danmakus:
        print(f"{dm.dm_time}s: {dm.text} (by {dm.crc32})")
```

## Video Download

### Complete Download Workflow

```python
import asyncio
import os
from bilibili_api import video, Credential, HEADERS, get_client

async def download_video(bvid: str, output: str = "video.mp4"):
    # Setup
    cred = Credential(sessdata="...", bili_jct="...", buvid3="...")
    v = video.Video(bvid=bvid, credential=cred)

    # Get download URLs
    download_data = await v.get_download_url(page_index=0)

    # Parse streams
    detecter = video.VideoDownloadURLDataDetecter(data=download_data)
    streams = detecter.detect_best_streams()

    # Check stream type
    if detecter.check_flv_mp4_stream():
        # FLV stream (single file with both video and audio)
        await download_file(streams[0].url, "temp.flv")
        os.system(f"ffmpeg -i temp.flv {output}")
        os.remove("temp.flv")
    else:
        # DASH streams (separate video and audio)
        await download_file(streams[0].url, "video_temp.m4s", "Video")
        await download_file(streams[1].url, "audio_temp.m4s", "Audio")

        # Merge with ffmpeg
        os.system(
            f"ffmpeg -i video_temp.m4s -i audio_temp.m4s "
            f"-vcodec copy -acodec copy {output}"
        )
        os.remove("video_temp.m4s")
        os.remove("audio_temp.m4s")

    print(f"Downloaded: {output}")

async def download_file(url: str, out: str, label: str = ""):
    client = get_client()
    dwn_id = await client.download_create(url, HEADERS)
    total = client.download_content_length(dwn_id)
    downloaded = 0

    with open(out, "wb") as f:
        while True:
            chunk = await client.download_chunk(dwn_id)
            if not chunk:
                break
            downloaded += f.write(chunk)
            print(f"{label} - {out} [{downloaded}/{total}]", end="\r")
    print()

asyncio.run(download_video("BV1AV411x7Gs"))
```

### Quality Enums

```python
from bilibili_api import video

# Video Quality
video.VideoQuality._4K_120FPS      # 125
video.VideoQuality._1080P_60FPS    # 116
video.VideoQuality._1080P_PLUS     # 112
video.VideoQuality._1080P          # 80
video.VideoQuality._720P_60FPS     # 74
video.VideoQuality._720P           # 64
video.VideoQuality._480P           # 32
video.VideoQuality._360P           # 16

# Audio Quality
video.AudioQuality._192K           # 30280
video.AudioQuality._132K           # 30232
video.AudioQuality._64K            # 30216

# Video Codecs
video.VideoCodecs.AVC              # HEPEC
video.VideoCodecs.HEV              # HEPEC
video.VideoCodecs.AV1              # HEPEC
```

## VideoOnlineMonitor (WebSocket)

Monitor real-time online count and danmaku:

```python
from bilibili_api import video
import asyncio

monitor = video.VideoOnlineMonitor(bvid="BV1AV411x7Gs")

@monitor.on('ONLINE')
async def on_online(event):
    print(f"Online: {event}")

@monitor.on('DANMAKU')
async def on_danmaku(event):
    print(f"Danmaku: {event}")

asyncio.run(monitor.connect())
```

## Module-Level Functions

```python
from bilibili_api import video

# Get video info by BV/AV without instantiating
info = await video.get_video_info(bvid="BVxxxxxxxx")

# AV/BV conversion
bvid = video.aid2bvid(170001)
aid = video.bvid2aid("BV17x411w7KC")
```

## Full API Reference

For complete method signatures and all available options, see:
`references/docs/modules/video.md`
