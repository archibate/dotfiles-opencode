# User Module Guide

## User Class

```python
from bilibili_api import user, Credential

# Create user instance
u = user.User(uid=660303135)

# With credentials (for self operations)
cred = Credential(sessdata="...", bili_jct="...")
u = user.User(uid=123456, credential=cred)
```

## Profile Methods

| Method | Description | Auth |
|--------|-------------|------|
| `get_user_info()` | Basic user profile | No |
| `get_relation_info()` | Follower/following counts | No |
| `get_up_stat()` | Uploader statistics | No |
| `get_live_info()` | Live streaming info | No |
| `get_space_notice()` | Space announcement | No |
| `get_top_videos()` | Pinned videos | No |
| `get_masterpiece()` | Masterpiece videos | No |

```python
async def get_user_profile():
    u = user.User(uid=660303135)
    info = await u.get_user_info()
    print(f"Name: {info['name']}")
    print(f"Sign: {info['sign']}")

    relation = await u.get_relation_info()
    print(f"Followers: {relation['follower']}")
    print(f"Following: {relation['following']}")
```

## Content Methods

| Method | Description | Auth |
|--------|-------------|------|
| `get_videos(tid, pn, ps, keyword, order)` | User's videos | No |
| `get_dynamics_new(offset, type_list)` | User's dynamics | No |
| `get_audios(order, pn, ps)` | User's audio | No |
| `get_articles(pn, ps, sort)` | User's articles | No |
| `get_cheese()` | Paid courses | No |
| `get_channel_series_list()` | Channel series | No |
| `get_favorites(page_index, page_size)` | Public favorites | No |

```python
async def get_user_videos():
    u = user.User(uid=660303135)
    result = await u.get_videos(pn=1, ps=30)
    for v in result["list"]["vlist"]:
        print(f"{v['title']} - {v['play']} views")
```

## Social Methods

| Method | Description | Auth |
|--------|-------------|------|
| `get_followers(pn, ps)` | Get followers list | No |
| `get_followings(pn, ps)` | Get following list | No |
| `get_self_same_followers()` | Mutual follows | Yes |
| `modify_relation(relation)` | Follow/unfollow/block | Yes |
| `get_elec_user_monthly()` | Monthly elec (charging) | No |

```python
from bilibili_api.user import RelationType

async def follow_user():
    cred = Credential(sessdata="...", bili_jct="...")
    u = user.User(uid=123456, credential=cred)

    # Follow
    await u.modify_relation(relation=RelationType.SUBSCRIBE)

    # Unfollow
    await u.modify_relation(relation=RelationType.UNSUBSCRIBE)

    # Remove from followers (break follow)
    await u.modify_relation(relation=RelationType.REMOVE_FANS)
```

## Enums

```python
from bilibili_api.user import (
    VideoOrder,      # Video sorting
    AudioOrder,      # Audio sorting
    ArticleOrder,    # Article sorting
    BangumiType,     # Bangumi type
    RelationType,    # Relation actions
    ChannelOrder,    # Channel sorting
)

# VideoOrder
VideoOrder.PUBDATE    # By publish date
VideoOrder.CLICK      # By views
VideoOrder.STOW       # By favorites

# RelationType
RelationType.SUBSCRIBE      # Follow
RelationType.UNSUBSCRIBE    # Unfollow
RelationType.REMOVE_FANS    # Remove follower
```

## Pagination Pattern

### Page-Based (Videos, Followers)

```python
async def get_all_videos(uid: int):
    u = user.User(uid=uid)
    page = 1
    all_videos = []

    while True:
        result = await u.get_videos(pn=page, ps=30)
        videos = result["list"]["vlist"]

        if not videos:
            break

        all_videos.extend(videos)
        total = result["page"]["count"]

        if len(all_videos) >= total:
            break

        page += 1

    return all_videos
```

### Offset-Based (Dynamics)

```python
async def get_all_dynamics(uid: int):
    u = user.User(uid=uid)
    offset = ""
    all_dynamics = []

    while True:
        result = await u.get_dynamics_new(offset=offset)

        if not result or "items" not in result:
            break

        all_dynamics.extend(result["items"])

        if result.get("has_more") != 1:
            break

        offset = result.get("offset", "")

    return all_dynamics
```

## Module-Level Functions (Self Operations)

These functions operate on the authenticated user:

```python
from bilibili_api import user, sync, Credential

async def self_operations():
    cred = Credential(sessdata="...", bili_jct="...")

    # Get own info
    info = await user.get_self_info(credential=cred)

    # Get watch history
    history = await user.get_self_history(credential=cred)

    # Get coin balance
    coins = await user.get_self_coins(credential=cred)

    # Get watch later list
    toview = await user.get_toview_list(credential=cred)

    # Get notifications
    events = await user.get_self_events(credential=cred)
```

## Full API Reference

For complete method signatures, see:
`references/docs/modules/user.md`
