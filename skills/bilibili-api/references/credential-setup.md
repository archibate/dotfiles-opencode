# Credential Setup

## Credential Class

The `Credential` class stores authentication cookies required for Bilibili API access.

```python
from bilibili_api import Credential

credential = Credential(
    sessdata="...",        # Required for GET (read) operations
    bili_jct="...",        # Required for POST (write) operations
    buvid3="...",          # Device ID v3 (auto-generated if omitted)
    buvid4="...",          # Device ID v4 (optional)
    dedeuserid="...",      # User UID (rarely needed)
    ac_time_value="...",   # For cookie refresh only
    proxy="...",           # Optional proxy for this credential
)
```

## Cookie Field Reference

| Field | Cookie Name | Purpose | When Required |
|-------|-------------|---------|---------------|
| `sessdata` | `SESSDATA` | User session for reading user data | GET operations on user-specific data |
| `bili_jct` | `bili_jct` | CSRF token for modifying data | POST operations (like, comment, upload) |
| `buvid3` | `buvid3` | Device fingerprint v3 | Some APIs require it; anti-bot |
| `buvid4` | `buvid4` | Device fingerprint v4 | Optional, related to risk control |
| `dedeuserid` | `DedeUserID` | User UID | Rarely needed |
| `ac_time_value` | (localStorage) | Token for cookie refresh | Only for `credential.refresh()` |

## Browser Extraction

Extract cookies from a logged-in browser session at `bilibili.com`:

### Chrome / Edge

1. Open bilibili.com and log in
2. Press `F12` to open DevTools
3. Go to **Application** tab (Chrome) or **应用程序** tab (Edge)
4. Navigate to **Storage → Cookies → https://www.bilibili.com**
5. Copy values for: `SESSDATA`, `bili_jct`, `buvid3`, `DedeUserID`

### Firefox

1. Open bilibili.com and log in
2. Press `F12` to open DevTools
3. Go to **Storage** tab
4. Navigate to **Cookies → https://www.bilibili.com**
5. Copy values for: `SESSDATA`, `bili_jct`, `buvid3`, `DedeUserID`

### ac_time_value (for cookie refresh)

1. Open bilibili.com while logged in
2. Press `F12` to open DevTools
3. Go to **Console** tab
4. Run: `window.localStorage.ac_time_value`
5. Copy the returned value

## Credential Validation

```python
# Check if fields are present
credential.has_sessdata()    # bool
credential.has_bili_jct()    # bool
credential.has_buvid3()      # bool
credential.has_buvid4()      # bool
credential.has_dedeuserid()  # bool
credential.has_ac_time_value()  # bool

# Raise exception if missing (useful for validation)
credential.raise_for_no_sessdata()
credential.raise_for_no_bili_jct()
credential.raise_for_no_buvid3()

# Get all cookies as dict
cookies = credential.get_cookies()
```

## Programmatic Login

### QR Code Login

```python
from bilibili_api import login_v2, sync
import time

async def qr_login():
    qr = login_v2.QrCodeLogin(platform=login_v2.QrCodeLoginChannel.WEB)
    await qr.generate_qrcode()

    # Print QR code to terminal
    print(qr.get_qrcode_terminal())

    # Poll until scanned
    while not qr.has_done():
        state = await qr.check_state()
        print(f"Status: {state}")
        time.sleep(1)

    # Get credential
    credential = qr.get_credential()
    print(credential.get_cookies())
    return credential

sync(qr_login())
```

### Password Login

Requires Geetest captcha verification:

```python
from bilibili_api import Geetest, login_v2, sync

async def password_login():
    # Complete Geetest captcha
    gee = Geetest()
    await gee.generate_test()
    gee.start_geetest_server()
    print(f"Open: {gee.get_geetest_server_url()}")

    while not gee.has_done():
        pass
    gee.close_geetest_server()

    # Login with password
    cred = await login_v2.login_with_password(
        username="phone_or_email",
        password="password",
        geetest=gee
    )

    # Handle security check if needed
    if isinstance(cred, login_v2.LoginCheck):
        # Additional verification required
        gee2 = Geetest()
        await gee2.generate_test(type_=GeetestType.VERIFY)
        # ... complete verification
        await cred.send_sms(gee2)
        code = input("SMS code: ")
        cred = await cred.complete_check(code)

    return cred
```

### SMS Login

```python
from bilibili_api import Geetest, login_v2, sync

async def sms_login():
    # Complete Geetest first
    gee = Geetest()
    await gee.generate_test()
    gee.start_geetest_server()
    print(f"Open: {gee.get_geetest_server_url()}")
    while not gee.has_done():
        pass
    gee.close_geetest_server()

    # Send SMS
    phone = login_v2.PhoneNumber("13800138000", "+86")
    captcha_id = await login_v2.send_sms(phonenumber=phone, geetest=gee)

    # Login with SMS code
    code = input("SMS code: ")
    cred = await login_v2.login_with_sms(
        phonenumber=phone,
        code=code,
        captcha_id=captcha_id
    )
    return cred
```

## Cookie Refresh

Refresh cookies before they expire. Requires `ac_time_value`:

```python
from bilibili_api import Credential, sync

credential = Credential(
    sessdata="...",
    bili_jct="...",
    ac_time_value="..."  # Required for refresh
)

# Check if refresh needed
needs_refresh = sync(credential.check_refresh())
print(f"Needs refresh: {needs_refresh}")

# Perform refresh
if needs_refresh:
    sync(credential.refresh())
    print("Cookies refreshed")
    print(credential.get_cookies())
```

**Notes:**
- Do not refresh too frequently
- If using credentials long-term, avoid logging into the same account in a browser (this invalidates cookies)
- After refresh, the new cookie values are updated in the `Credential` instance

## Security Best Practices

1. **Never hardcode credentials** in source code
2. **Use environment variables** for credential storage:

```python
import os
from bilibili_api import Credential

credential = Credential(
    sessdata=os.environ.get("BILI_SESSDATA"),
    bili_jct=os.environ.get("BILI_JCT"),
    buvid3=os.environ.get("BILI_BUVID3"),
)
```

3. **Use `.env` files** (add to `.gitignore`):

```python
# .env
BILI_SESSDATA=your_sessdata
BILI_JCT=your_bili_jct
BILI_BUVID3=your_buvid3
```

```python
# Load from .env
from dotenv import load_dotenv
load_dotenv()
```

4. **Rotate credentials** periodically
5. **Use minimal permissions** — only include fields needed for your use case
