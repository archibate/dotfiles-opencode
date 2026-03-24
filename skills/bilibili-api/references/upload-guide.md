# Upload Guide

## Video Upload Workflow

### Step 1: Create Upload Pages

```python
from bilibili_api import video_uploader

page = video_uploader.VideoUploaderPage(
    path="video.mp4",          # Path to video file
    title="Video Title",       # Page title (for multi-part)
    description="Description", # Page description
)
```

### Step 2: Create Video Metadata

```python
from bilibili_api import video_uploader, Picture

meta = video_uploader.VideoMeta(
    tid=130,                    # Zone/category ID
    title="My Video Title",     # Video title
    tags=["tag1", "tag2"],      # Tags (comma-separated string or list)
    desc="Video description",   # Description
    cover=Picture.from_file("cover.png"),  # Cover image
    no_reprint=True,            # Disable reprinting
    open_elec=False,            # Enable charging
    # ... more options
)
```

### VideoMeta Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tid` | int | Yes | Zone ID (use `video_zone` module) |
| `title` | str | Yes | Video title (max 80 chars) |
| `tags` | list/str | Yes | Tags |
| `desc` | str | No | Description |
| `cover` | Picture/str | No | Cover image |
| `copyright` | int | No | 1=original, 2=reprint |
| `source` | str | No | Source URL (for reprints) |
| `no_reprint` | bool | No | Disable reprinting |
| `open_elec` | bool | No | Enable charging |
| `dtime` | int | No | Scheduled publish timestamp |
| `interactive` | int | No | Interactive video flag |

### Step 3: Create Uploader and Monitor Events

```python
from bilibili_api import Credential

credential = Credential(sessdata="...", bili_jct="...", buvid3="...")

uploader = video_uploader.VideoUploader(
    pages=[page],
    meta=meta,
    credential=credential,
    line=video_uploader.Lines.QN,  # Optional: force upload line
)

@uploader.on("__ALL__")
async def on_event(data):
    print(f"Event: {data}")
```

### Upload Events

| Event | Description |
|-------|-------------|
| `PREUPLOAD` | Pre-upload started |
| `PREUPLOAD_END` | Pre-upload finished |
| `UPLOADING` | Upload progress |
| `UPLOADING_END` | Upload part finished |
| `PRE_PAGE` | Starting new page |
| `SUBMIT` | Submitting to Bilibili |
| `SUCCESS` | Upload successful |
| `FAILED` | Upload failed |

### Step 4: Start Upload

```python
async def upload_video():
    await uploader.start()
    print("Upload complete!")

from bilibili_api import sync
sync(upload_video())
```

## Complete Upload Example

```python
from bilibili_api import sync, video_uploader, Credential, Picture

async def main():
    credential = Credential(
        sessdata="your_sessdata",
        bili_jct="your_bili_jct",
        buvid3="your_buvid3"
    )

    # Create metadata
    meta = video_uploader.VideoMeta(
        tid=130,  # Music zone
        title="My Awesome Video",
        tags=["music", "cover"],
        desc="This is my video description",
        cover=Picture.from_file("cover.png"),
        no_reprint=True,
    )

    # Verify metadata locally (optional)
    await meta.verify(credential=credential)

    # Create page
    page = video_uploader.VideoUploaderPage(
        path="video.mp4",
        title="Part 1",
    )

    # Create uploader
    uploader = video_uploader.VideoUploader(
        pages=[page],
        meta=meta,
        credential=credential,
    )

    # Monitor progress
    @uploader.on("UPLOADING")
    async def on_progress(data):
        print(f"Progress: {data}")

    @uploader.on("SUCCESS")
    async def on_success(data):
        print(f"Video uploaded! BV: {data['bvid']}")

    @uploader.on("FAILED")
    async def on_failed(data):
        print(f"Upload failed: {data}")

    # Start upload
    await uploader.start()

sync(main())
```

## Upload Lines

Choose upload server for better speed:

```python
from bilibili_api import video_uploader

# Available lines
video_uploader.Lines.BDA2   # Baidu
video_uploader.Lines.QN     # Qiniu
video_uploader.Lines.WS     # Wangsu
video_uploader.Lines.BLDSA  # Bilibili

# Auto-select (default)
uploader = video_uploader.VideoUploader(pages, meta, credential)

# Force specific line
uploader = video_uploader.VideoUploader(
    pages, meta, credential,
    line=video_uploader.Lines.QN
)
```

## Multi-Part Videos

```python
pages = [
    video_uploader.VideoUploaderPage(
        path="part1.mp4",
        title="Part 1: Introduction",
    ),
    video_uploader.VideoUploaderPage(
        path="part2.mp4",
        title="Part 2: Main Content",
    ),
    video_uploader.VideoUploaderPage(
        path="part3.mp4",
        title="Part 3: Conclusion",
    ),
]

uploader = video_uploader.VideoUploader(pages, meta, credential)
```

## Video Editing

Edit existing uploaded videos:

```python
from bilibili_api import video_uploader, Credential

async def edit_video():
    credential = Credential(sessdata="...", bili_jct="...")

    editor = video_uploader.VideoEditor(
        bvid="BVxxxxxxxx",
        meta=video_uploader.VideoMeta(
            tid=130,
            title="New Title",
            tags=["new", "tags"],
        ),
        credential=credential,
    )

    @editor.on("__ALL__")
    async def on_event(data):
        print(data)

    await editor.edit()

from bilibili_api import sync
sync(edit_video())
```

## Audio Upload

```python
from bilibili_api import audio_uploader, Credential, Picture

async def upload_audio():
    credential = Credential(sessdata="...", bili_jct="...")

    meta = audio_uploader.SongMeta(
        title="My Song",
        cover=Picture.from_file("cover.png"),
        tid=130,  # Audio category
        desc="Song description",
    )

    uploader = audio_uploader.AudioUploader(
        path="song.mp3",
        meta=meta,
        credential=credential,
    )

    @uploader.on("__ALL__")
    async def on_event(data):
        print(data)

    await uploader.start()

from bilibili_api import sync
sync(upload_audio())
```

## Full API Reference

For complete method signatures, see:
- `references/docs/modules/video_uploader.md`
- `references/docs/modules/audio_uploader.md`
