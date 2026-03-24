# API Modules Reference

Complete list of all 42 modules in bilibili-api v17.4.1.

## Content Modules

| Module | Chinese | Key Classes | Key Methods | Auth |
|--------|---------|-------------|-------------|------|
| `video` | 视频 | `Video`, `VideoDownloadURLDataDetecter`, `VideoOnlineMonitor` | `get_info()`, `get_download_url()`, `like()`, `send_danmaku()` | Actions need auth |
| `bangumi` | 番剧 | `Bangumi`, `IndexFilter` | `get_info()`, `get_episodes()`, `get_stat()` | Some actions |
| `article` | 专栏 | `Article`, `ArticleList` | `get_info()`, `get_content()`, `like()`, `add_coins()` | Actions need auth |
| `audio` | 音频 | `Audio`, `AudioList` | `get_info()`, `get_download_url()`, `like()` | Actions need auth |
| `manga` | 漫画 | `Manga`, `MangaIndexFilter` | `get_info()`, `get_images()`, `like()` | Some actions |
| `cheese` | 课程 | `CheeseList`, `CheeseVideo` | `get_info()`, `get_list()`, `get_video_info()` | Paid content |
| `opus` | 图文 | `Opus` | `get_info()`, `get_content()` | No |
| `note` | 笔记 | `Note` | `get_info()`, `get_content()` | No |
| `interactive_video` | 互动视频 | `InteractiveVideo`, `InteractiveGraph` | `get_info()`, `get_graph_version()` | No |
| `ass` | ASS字幕 | (functions) | `create_ass_from_danmaku()` | No |

## Social Modules

| Module | Chinese | Key Classes | Key Methods | Auth |
|--------|---------|-------------|-------------|------|
| `user` | 用户 | `User` | `get_user_info()`, `get_videos()`, `get_dynamics_new()`, `modify_relation()` | Some actions |
| `dynamic` | 动态 | `Dynamic` | `get_info()`, `like()`, `repost()`, `delete()` | Actions need auth |
| `comment` | 评论 | `Comment` | `get_comments()`, `send_comment()`, `like()`, `delete()` | Actions need auth |
| `session` | 会话 | (functions) | `get_sessions()`, `send_msg()`, `get_msg()` | Yes |
| `emoji` | 表情 | (functions) | `get_emoji_list()`, `get_emoji_url()` | No |

## Discovery Modules

| Module | Chinese | Key Classes | Key Methods | Auth |
|--------|---------|-------------|-------------|------|
| `search` | 搜索 | `SearchObjectType`, various enums | `search()`, `search_by_type()` | No |
| `hot` | 热门 | (functions) | `get_hot_videos()`, `get_hot_bvids()` | No |
| `rank` | 排行 | (functions) | `get_rank()`, `get_music_rank()` | No |
| `homepage` | 主页 | (functions) | `get_popular()`, `get_recommend()` | No |
| `video_zone` | 视频分区 | (functions) | `get_zone_info()`, `get_zone_list()` | No |
| `channel_series` | 合集与列表 | `ChannelSeries` | `get_info()`, `get_videos()` | No |
| `topic` | 话题 | (functions) | `get_topic_info()`, `get_topic_cards()` | No |
| `video_tag` | 视频标签 | (functions) | `get_tag_info()`, `get_tag_videos()` | No |

## Live Modules

| Module | Chinese | Key Classes | Key Methods | Auth |
|--------|---------|-------------|-------------|------|
| `live` | 直播 | `LiveRoom`, `LiveDanmaku` | `get_room_info()`, `send_danmaku()`, `send_gift_gold()` | Actions need auth |
| `live_area` | 直播分区 | (functions) | `get_area_list()`, `get_area_info()` | No |
| `watchroom` | 放映室 | `WatchRoom` | `get_info()`, `join()`, `send_message()` | Yes |

## Upload Modules

| Module | Chinese | Key Classes | Key Methods | Auth |
|--------|---------|-------------|-------------|------|
| `video_uploader` | 视频上传 | `VideoUploader`, `VideoMeta`, `VideoUploaderPage`, `VideoEditor` | `start()`, `edit()` | Yes |
| `audio_uploader` | 音频上传 | `AudioUploader`, `SongMeta` | `start()` | Yes |

## Account Modules

| Module | Chinese | Key Classes | Key Methods | Auth |
|--------|---------|-------------|-------------|------|
| `login_v2` | 登录 | `QrCodeLogin`, `PhoneNumber`, `LoginCheck` | `login_with_password()`, `login_with_sms()` | N/A |
| `creative_center` | 创作中心 | (functions) | `get_manage_overview()`, `get_videos()` | Yes |
| `favorite_list` | 收藏夹 | `FavoriteList` | `get_content()`, `add_video()`, `delete_video()` | Actions need auth |
| `garb` | 装扮 | (functions) | `get_garb_info()`, `get_suit_list()` | No |
| `black_room` | 小黑屋 | (functions) | `get_blocked_list()`, `get_blocked_info()` | No |

## Other Modules

| Module | Chinese | Key Classes | Key Methods | Auth |
|--------|---------|-------------|-------------|------|
| `activity` | 活动 | (functions) | `get_activity_info()` | No |
| `app` | 应用程序 | (functions) | `get_app_info()` | No |
| `article_category` | 专栏分类 | (functions) | `get_categories()` | No |
| `client` | 终端 | (functions) | `get_client_info()` | No |
| `festival` | 节日 | (functions) | `get_festival_info()` | No |
| `game` | 游戏 | (functions) | `get_game_info()`, `get_game_list()` | No |
| `music` | 音乐 | `Music` | `get_info()`, `get_music_detail()` | No |
| `show` | 展出 | (functions) | `get_show_list()`, `get_show_info()` | No |
| `vote` | 投票 | (functions) | `get_vote_info()`, `create_vote()` | Actions need auth |

## Utility Exports (from bilibili_api)

| Export | Description |
|--------|-------------|
| `Credential` | Authentication class |
| `sync()` | Async-to-sync wrapper |
| `Picture` | Image handling |
| `Danmaku`, `SpecialDanmaku` | Danmaku classes |
| `DmMode`, `DmFontSize` | Danmaku enums |
| `AsyncEvent` | Event system base class |
| `Geetest`, `GeetestType` | Captcha handling |
| `aid2bvid()`, `bvid2aid()` | ID conversion |
| `parse_link()`, `ResourceType` | Link parsing |
| `get_real_url()` | Short URL resolution |
| `request_settings` | Global settings |
| `request_log` | Request logging |
| `select_client()`, `get_client()` | HTTP client management |
| `get_buvid()`, `recalculate_wbi()` | Anti-spider utilities |

## Exceptions

| Exception | When Raised |
|-----------|-------------|
| `ApiException` | Base API exception |
| `ArgsException` | Invalid arguments |
| `NetworkException` | Network/HTTP errors |
| `ResponseCodeException` | API returned error code |
| `LoginError` | Login failed |
| `GeetestException` | Captcha error |
| `CookiesRefreshException` | Cookie refresh failed |
| `VideoUploadException` | Upload error |
| `LiveException` | Live streaming error |
| `DanmakuClosedException` | Danmaku connection closed |
| `WbiRetryTimesExceedException` | WBI retries exhausted |
| `CredentialNo*Exception` | Missing credential fields |

## Full Documentation

For exhaustive API signatures and all methods, consult:
- `references/docs/modules/<module>.md` — Full API reference
- `references/docs/examples/<module>.md` — Usage examples
