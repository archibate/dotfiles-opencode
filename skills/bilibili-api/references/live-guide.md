# Live Module Guide

## LiveRoom Class

```python
from bilibili_api import live, Credential

# By room display ID
room = live.LiveRoom(room_display_id=22544798)

# With credentials (for actions)
cred = Credential(sessdata="...", bili_jct="...")
room = live.LiveRoom(room_display_id=123456, credential=cred)
```

### Room Info Methods

| Method | Description |
|--------|-------------|
| `get_room_info()` | Room details (title, status, etc.) |
| `get_room_play_info()` | Stream info (quality, codec) |
| `get_room_play_url(quality)` | Direct stream URL |
| `get_chat_conf()` | Danmaku server config |
| `get_fan_model()` | Fan badge info |
| `get_self_info()` | Self info in room (requires auth) |

```python
async def get_room_details():
    room = live.LiveRoom(room_display_id=22544798)
    info = await room.get_room_info()
    print(f"Title: {info['room_info']['title']}")
    print(f"Live: {info['room_info']['live_status'] == 1}")
    print(f"Viewers: {info['room_info']['online']}")
```

### Room Action Methods (Require Credential)

| Method | Description |
|--------|-------------|
| `send_danmaku(danmaku)` | Send danmaku |
| `send_gift_gold(uid, gift_id, gift_num, price)` | Send gold gift |
| `send_gift_silver(gift_id, gift_num)` | Send silver gift |
| `sign()` | Check-in |
| `ban_user(uid)` | Ban user from room |
| `unban_user(uid)` | Unban user |

```python
from bilibili_api import Danmaku

async def send_danmaku():
    cred = Credential(sessdata="...", bili_jct="...")
    room = live.LiveRoom(room_display_id=123456, credential=cred)

    dm = Danmaku(text="Hello!")
    await room.send_danmaku(dm)
```

## LiveDanmaku Class (WebSocket)

Real-time event stream for live rooms:

```python
from bilibili_api import live

room = live.LiveDanmaku(room_display_id=22544798)

@room.on("DANMU_MSG")
async def on_danmaku(event):
    data = event["data"]["info"]
    user = data[2][1]      # Username
    text = data[1]         # Danmaku content
    print(f"{user}: {text}")

@room.on("SEND_GIFT")
async def on_gift(event):
    data = event["data"]["data"]
    user = data["uname"]
    gift = data["giftName"]
    num = data["num"]
    print(f"{user} sent {num}x {gift}")

await room.connect()
```

### Available Events

| Event | Description |
|-------|-------------|
| `DANMU_MSG` | Danmaku message |
| `SEND_GIFT` | Gift sent |
| `GUARD_BUY` | Guard (membership) purchase |
| `SUPER_CHAT_MESSAGE` | Super chat (paid message) |
| `LIVE` | Stream started |
| `PREPARING` | Stream ending |
| `INTERACT_WORD` | User entered room |
| `LIKE_INFO_V3_CLICK` | Like clicked |
| `WATCHED_CHANGE` | Viewer count changed |

### Event Data Structure

```python
# DANMU_MSG
event["data"]["info"][1]      # Danmaku text
event["data"]["info"][2][0]   # Sender UID
event["data"]["info"][2][1]   # Sender username

# SEND_GIFT
event["data"]["data"]["uname"]      # Sender name
event["data"]["data"]["giftName"]   # Gift name
event["data"]["data"]["num"]        # Quantity
event["data"]["data"]["price"]      # Price per gift

# SUPER_CHAT_MESSAGE
event["data"]["data"]["user_info"]["uname"]  # Sender
event["data"]["data"]["message"]             # Message
event["data"]["data"]["price"]               # Amount
```

## Auto-Reply Bot Example

```python
from bilibili_api import Credential, Danmaku, sync
from bilibili_api.live import LiveDanmaku, LiveRoom

ROOMID = 123456
credential = Credential(sessdata="...", bili_jct="...")

monitor = LiveDanmaku(ROOMID, credential=credential)
sender = LiveRoom(ROOMID, credential=credential)
UID = sync(sender.get_room_info())["room_info"]["uid"]

@monitor.on("DANMU_MSG")
async def reply(event):
    uid = event["data"]["info"][2][0]
    if uid == UID:  # Ignore own messages
        return

    msg = event["data"]["info"][1]
    if msg == "你好":
        await sender.send_danmaku(Danmaku("你好！"))

sync(monitor.connect())
```

## Gift Statistics Example

```python
from collections import defaultdict
from bilibili_api import live, sync

user_gifts = defaultdict(lambda: defaultdict(int))
room = live.LiveDanmaku(22544798)

@room.on("SEND_GIFT")
async def track_gifts(event):
    data = event["data"]["data"]
    user = data["uname"]
    gift = data["giftName"]
    num = data["num"]
    user_gifts[user][gift] += num

@room.on("DANMU_MSG")
async def print_stats(event):
    msg = event["data"]["info"][1]
    if msg == "!stats":
        for user, gifts in user_gifts.items():
            print(f"{user}: {dict(gifts)}")

sync(room.connect())
```

## Stream Quality Enums

```python
from bilibili_api import live

# Resolution
live.ScreenResolution.ORIGINAL    # Original
live.ScreenResolution._240P       # 240p
live.ScreenResolution._360P       # 360p
live.ScreenResolution._480P       # 480p
live.ScreenResolution._720P       # 720p
live.ScreenResolution._1080P      # 1080p
live.ScreenResolution._1080P_60   # 1080p 60fps
live.ScreenResolution._4K         # 4K

# Protocol
live.LiveProtocol.HTTP_HLS        # HLS
live.LiveProtocol.HTTP_FLV        # FLV
live.LiveProtocol.WS_FLV          # WebSocket FLV

# Codec
live.LiveCodec.AVC                # H.264
live.LiveCodec.HEVC               # H.265
```

## Full API Reference

For complete method signatures, see:
`references/docs/modules/live.md`
