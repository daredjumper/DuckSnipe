"""
DuckSnipe API
Handles asynchronous username validation with Roblox API
"""

import asyncio
import aiohttp
from config import AVAILABLE_SNIPES
from utils import log_message

async def validate_username(session, username, log_name="username_check"):
    """Check if a username is available on Roblox"""
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
    
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            data = await resp.json()
            code = data.get('code', -1)
            
            messages = {
                0: f"✓ {username} is available!",
                1: f"✗ {username} is taken.",
                2: f"✗ {username} is inappropriate.",
                10: f"✗ {username} may contain private info."
            }
            
            message = messages.get(code, f"? {username} returned unknown code: {code}")
            print(message)
            log_message(log_name, message)
            
            if code == 0:
                AVAILABLE_SNIPES.append(username)
                
    except asyncio.TimeoutError:
        msg = f"⚠ Timeout checking {username}"
        print(msg)
        log_message(log_name, msg)
    except Exception as e:
        msg = f"⚠ Error checking {username}: {e}"
        print(msg)
        log_message(log_name, msg)

async def validate_usernames_concurrent(usernames, log_name="username_check"):
    """Validate multiple usernames concurrently"""
    if not usernames:
        print("No usernames to check!")
        return
    
    print(f"Checking {len(usernames)} usernames...\n")
    
    async with aiohttp.ClientSession() as session:
        tasks = [validate_username(session, u, log_name) for u in usernames]
        await asyncio.gather(*tasks)
    
    if AVAILABLE_SNIPES:
        print(f"\n✓ Found {len(AVAILABLE_SNIPES)} available usernames!")
    else:
        print("\n✗ No available usernames found.")