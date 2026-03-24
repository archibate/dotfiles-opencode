#!/usr/bin/env python3
"""
bilibili-api Credential Check Script

Validates Bilibili API credentials from environment variables.

Usage:
    export BILI_SESSDATA="your_sessdata"
    export BILI_JCT="your_bili_jct"
    export BILI_BUVID3="your_buvid3"
    uv run python credential_check.py
"""

import os
import asyncio
from bilibili_api import Credential, user


def check_env_vars():
    """Check if required environment variables are set."""
    required = ["BILI_SESSDATA", "BILI_JCT", "BILI_BUVID3"]
    missing = [v for v in required if not os.environ.get(v)]

    if missing:
        print(f"Missing environment variables: {', '.join(missing)}")
        print("\nSet them with:")
        print("  export BILI_SESSDATA='your_sessdata'")
        print("  export BILI_JCT='your_bili_jct'")
        print("  export BILI_BUVID3='your_buvid3'")
        return False

    return True


async def validate_credential():
    """Validate credential by making an authenticated API call."""
    print("=== Bilibili Credential Check ===\n")

    # Check environment
    if not check_env_vars():
        return False

    # Create credential
    credential = Credential(
        sessdata=os.environ["BILI_SESSDATA"],
        bili_jct=os.environ["BILI_JCT"],
        buvid3=os.environ["BILI_BUVID3"],
    )

    # Check fields
    print("Checking credential fields...")
    print(f"  sessdata: {'✓' if credential.has_sessdata() else '✗'}")
    print(f"  bili_jct: {'✓' if credential.has_bili_jct() else '✗'}")
    print(f"  buvid3:   {'✓' if credential.has_buvid3() else '✗'}")

    # Check optional fields
    ac_time = os.environ.get("BILI_AC_TIME_VALUE")
    if ac_time:
        credential = Credential(
            sessdata=os.environ["BILI_SESSDATA"],
            bili_jct=os.environ["BILI_JCT"],
            buvid3=os.environ["BILI_BUVID3"],
            ac_time_value=ac_time,
        )
        print(f"  ac_time_value: {'✓' if credential.has_ac_time_value() else '✗'}")

    print()

    # Test API call
    print("Testing authenticated API call...")
    try:
        info = await user.get_self_info(credential=credential)
        print(f"  ✓ Successfully authenticated!")
        print(f"  Username: {info['data']['name']}")
        print(f"  UID: {info['data']['mid']}")
        print(f"  Level: {info['data']['level']}")
    except Exception as e:
        print(f"  ✗ Authentication failed: {e}")
        return False

    # Check if refresh needed
    if credential.has_ac_time_value():
        print("\nChecking cookie refresh status...")
        try:
            needs_refresh = await credential.check_refresh()
            if needs_refresh:
                print("  ⚠ Cookies may need refresh soon")
            else:
                print("  ✓ Cookies are fresh")
        except Exception as e:
            print(f"  Could not check refresh status: {e}")

    print("\n=== Credential Check Complete ===")
    return True


if __name__ == "__main__":
    success = asyncio.run(validate_credential())
    exit(0 if success else 1)
