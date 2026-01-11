"""
DuckSnipe API
Handles asynchronous username validation with Roblox API
"""

import asyncio
import aiohttp
from datetime import datetime
from colorama import Fore, Style


from config import (AVAILABLE_SNIPES, AVAILABLE_FILE, 
                    MAX_CONCURRENT_REQUESTS, REQUEST_DELAY)
from utils import log_message, save_rate_limit_alert


RATE_LIMIT_DETECTED = False

async def validate_username(session, username, log_name="username_check"):
    """Check if a username is available on Roblox"""
    global RATE_LIMIT_DETECTED
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
    
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            
            if resp.status == 429:
                RATE_LIMIT_DETECTED = True
                msg = f"{Fore.RED}⚠ RATE LIMITED! Received 429 status code for {username}"
                print(msg)
                log_message(log_name, msg)
                log_message("rate_limit", msg)
                save_rate_limit_alert("429 - Too Many Requests", username)
                return
            
            elif resp.status == 403:
                RATE_LIMIT_DETECTED = True
                msg = f"{Fore.RED}⚠ ACCESS BLOCKED! Received 403 status code for {username}"
                print(msg)
                log_message(log_name, msg)
                log_message("rate_limit", msg)
                save_rate_limit_alert("403 - Forbidden/Blocked", username)
                return
            
            elif resp.status != 200:
                msg = f"{Fore.YELLOW}⚠ Unexpected status {resp.status} for {username}"
                print(msg)
                log_message(log_name, msg)
                log_message("errors", msg)
                return
            
            data = await resp.json()
            code = data.get('code', -1)
            
            if code == 0:
                message = f"{Fore.GREEN}✓ {username} is available!{Style.RESET_ALL}"
                AVAILABLE_SNIPES.append(username)
                save_available_username(username)
            elif code == 1:
                message = f"{Fore.RED}✗ {username} is taken.{Style.RESET_ALL}"
            elif code == 2:
                message = f"{Fore.YELLOW}✗ {username} is inappropriate.{Style.RESET_ALL}"
            elif code == 10:
                message = f"{Fore.YELLOW}✗ {username} may contain private info.{Style.RESET_ALL}"
            else:
                message = f"{Fore.CYAN}? {username} returned unknown code: {code}{Style.RESET_ALL}"
            
            print(message)
            log_message(log_name, message)
                
    except asyncio.TimeoutError:
        msg = f"{Fore.YELLOW}⚠ Timeout checking {username}"
        print(msg)
        log_message(log_name, msg)
        log_message("timeouts", msg)
    except aiohttp.ClientError as e:
        msg = f"{Fore.YELLOW}⚠ Connection error checking {username}: {e}"
        print(msg)
        log_message(log_name, msg)
        log_message("connection_errors", msg)
    except Exception as e:
        msg = f"{Fore.RED}⚠ Error checking {username}: {e}"
        print(msg)
        log_message(log_name, msg)
        log_message("errors", msg)

def save_available_username(username):
    """Save available username to file with timestamp"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(AVAILABLE_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {username}\n")
    except Exception as e:
        print(f"{Fore.YELLOW}Warning: Could not save to {AVAILABLE_FILE}: {e}")

async def validate_usernames_concurrent(usernames, log_name="username_check"):
    """Validate multiple usernames concurrently with rate limiting"""
    global RATE_LIMIT_DETECTED
    RATE_LIMIT_DETECTED = False
    
    
    from config import MAX_CONCURRENT_REQUESTS, REQUEST_DELAY
    
    if not usernames:
        print(f"{Fore.RED}No usernames to check!")
        return
    
    print(f"{Fore.CYAN}Checking {len(usernames)} usernames...{Style.RESET_ALL}\n")
    log_message(log_name, f"Starting check of {len(usernames)} usernames")
    
    
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    
    async def validate_with_semaphore(session, username):
        async with semaphore:
            await validate_username(session, username, log_name)
            await asyncio.sleep(REQUEST_DELAY)
    
    async with aiohttp.ClientSession() as session:
        tasks = [validate_with_semaphore(session, u) for u in usernames]
        await asyncio.gather(*tasks)
    
    if RATE_LIMIT_DETECTED:
        alert_msg = "\n" + "="*50 + f"\n{Fore.RED}⚠ RATE LIMITING DETECTED!{Style.RESET_ALL}\n" + "="*50
        print(alert_msg)
        print(f"{Fore.YELLOW}Recommendations:")
        print("1. Wait 5-10 minutes before trying again")
        print("2. Use 'settings' command to lower MAX_CONCURRENT_REQUESTS")
        print(f"3. Use 'settings' command to increase REQUEST_DELAY{Style.RESET_ALL}")
        print("="*50 + "\n")
        
        log_message("rate_limit", alert_msg)
        log_message("rate_limit", "RECOMMENDATIONS:")
        log_message("rate_limit", "1. Wait 5-10 minutes before trying again")
        log_message("rate_limit", "2. Lower MAX_CONCURRENT_REQUESTS")
        log_message("rate_limit", "3. Increase REQUEST_DELAY")
    
    if AVAILABLE_SNIPES:
        success_msg = f"Found {len(AVAILABLE_SNIPES)} available usernames!"
        print(f"\n{Fore.GREEN}✓ {success_msg}")
        print(f"✓ Saved to: {AVAILABLE_FILE}{Style.RESET_ALL}")
        log_message(log_name, success_msg)
    else:
        fail_msg = "No available usernames found."
        print(f"\n{Fore.RED}✗ {fail_msg}{Style.RESET_ALL}")
        log_message(log_name, fail_msg)