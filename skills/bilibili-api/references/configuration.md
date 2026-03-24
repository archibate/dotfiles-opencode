# Configuration

## Request Settings

```python
from bilibili_api import request_settings
```

### Available Settings

| Setting | Type | Default | curl_cffi | aiohttp | httpx | Description |
|---------|------|---------|-----------|---------|-------|-------------|
| `proxy` | str | `""` | ✅ | ✅ | ✅ | HTTP/HTTPS proxy URL |
| `timeout` | float | `30.0` | ✅ | ✅ | ✅ | Request timeout in seconds |
| `verify_ssl` | bool | `True` | ✅ | ✅ | ✅ | Verify SSL certificates |
| `trust_env` | bool | `True` | ✅ | ✅ | ✅ | Use environment proxy settings |
| `impersonate` | str | `""` | ✅ | ❌ | ❌ | Browser fingerprint to mimic |
| `http2` | bool | `False` | ✅ | ❌ | ✅ | Enable HTTP/2 |
| `wbi_retry_times` | int | `3` | \\ | \\ | \\ | WBI signature retry limit |
| `enable_auto_buvid` | bool | `True` | \\ | \\ | \\ | Auto-generate buvid |
| `enable_bili_ticket` | bool | `False` | \\ | \\ | \\ | Auto-generate bili_ticket |

### Setting Methods

```python
# Set individual settings
request_settings.set_proxy("http://127.0.0.1:7890")
request_settings.set_timeout(60.0)
request_settings.set_verify_ssl(False)
request_settings.set_trust_env(True)

# Generic setter
request_settings.set("impersonate", "chrome131")

# Get settings
proxy = request_settings.get_proxy()
timeout = request_settings.get("timeout")
all_settings = request_settings.get_all()
```

## Proxy Configuration

Two methods to configure proxy:

### Method 1: Global Proxy

```python
request_settings.set_proxy("http://127.0.0.1:7890")

# With authentication
request_settings.set_proxy("http://user:pass@proxy.example.com:8080")
```

### Method 2: Per-Credential Proxy

```python
from bilibili_api import Credential

credential = Credential(
    sessdata="...",
    bili_jct="...",
    proxy="http://127.0.0.1:7890"
)
```

## HTTP Client Selection

Three HTTP backends available:

| Client | Priority | Request | Stream | WebSocket | Notes |
|--------|----------|---------|--------|-----------|-------|
| `curl_cffi` | 3 (highest) | ✅ | ✅ | ✅ | Supports TLS/JA3 impersonation |
| `aiohttp` | 2 | ✅ | ✅ | ✅ | Pure Python, most compatible |
| `httpx` | 1 (lowest) | ✅ | ✅ | ❌ | No WebSocket support |

### Switch Client

```python
from bilibili_api import select_client, get_selected_client

select_client("curl_cffi")
print(get_selected_client())  # "curl_cffi"
```

### Access Session

```python
from bilibili_api import get_session, set_session

# Get the underlying session
session = get_session()  # e.g., httpx.AsyncClient

# Use custom session
import httpx
custom_session = httpx.AsyncClient(timeout=120.0)
set_session(custom_session)
```

### Browser Impersonation (curl_cffi)

```python
select_client("curl_cffi")
request_settings.set("impersonate", "chrome131")
# Available: chrome99, chrome100, chrome101, ..., edge99, safari15_3, etc.
```

## Request Logging

```python
from bilibili_api import request_log

# Enable logging
request_log.set_on(True)

# Filter by event types
request_log.set_on_events(["API_REQUEST", "API_RESPONSE"])

# Ignore certain events
request_log.set_ignore_events(["WS_RECV"])
```

### Event Types

- `API_REQUEST` — API call initiated
- `API_RESPONSE` — API response received
- `ANTI_SPIDER` — Anti-spider measures triggered
- `WS_CONNECT` — WebSocket connected
- `WS_RECV` — WebSocket message received
- `WS_SEND` — WebSocket message sent
- `WS_CLOSE` — WebSocket closed

## Anti-Spider Measures

### WBI Signature

Bilibili uses WBI signatures to protect certain APIs. The library handles this automatically.

```python
from bilibili_api import recalculate_wbi

# Manual WBI key refresh (usually not needed)
await recalculate_wbi()

# Set retry limit
request_settings.set_wbi_retry_times(10)  # default: 3
```

### BUVID Auto-Generation

```python
from bilibili_api import refresh_buvid

# Enable/disable auto-generation
request_settings.set_enable_auto_buvid(True)  # default: True

# Manual refresh
await refresh_buvid()
```

### Bili Ticket

```python
from bilibili_api import refresh_bili_ticket

# Enable bili_ticket
request_settings.set_enable_bili_ticket(True)  # default: False

# Manual refresh
await refresh_bili_ticket()
```

## Custom Client

Extend `BiliAPIClient` to use a custom HTTP backend:

```python
from bilibili_api import BiliAPIClient, register_client

class MyClient(BiliAPIClient):
    def __init__(self, proxy="", timeout=0.0, verify_ssl=True, trust_env=True, session=None):
        super().__init__(proxy, timeout, verify_ssl, trust_env, session)
        # Custom initialization

    async def request(self, method, url, params={}, data={}, files={}, headers={}, cookies={}, allow_redirects=True):
        # Implement request logic
        pass

    # Implement other required methods...

register_client("my_client", MyClient, {"custom_setting": "default_value"})
```

See `<project_root>/bilibili_api/clients/` for reference implementations.
