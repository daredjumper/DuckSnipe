"""
DuckSnipe Commands
All command implementations and handlers
"""

import random
import asyncio
import string
from time import perf_counter
from colorama import Fore, Back, Style
import config
from utils import safe_file_write, safe_file_read, log_message, sync_custom_words, save_settings
from api import validate_usernames_concurrent

def add_word(word):
    """Add a custom word to the wordlist"""
    start_time = perf_counter()
    
    word = word.strip()
    
    if not word:
        print(f"{Fore.RED}Error: Word cannot be empty!")
        return
    
    if word in config.CUSTOM_WORDS:
        print(f"{Fore.YELLOW}'{word}' is already in custom words!")
        return
    
    if safe_file_write(config.WORDS_FILE, f"{word},"):
        sync_custom_words()
        msg = f"✓ Added word '{word}' to custom wordlist"
        print(f"{Fore.GREEN}{msg}")
        log_message("addword", msg)
        
        elapsed = (perf_counter() - start_time) * 1000
        log_message("addword", f"Command completed in {elapsed:.2f}ms")
    else:
        print(f"{Fore.RED}✗ Failed to add word")

def generate_pass(username):
    """Generate a random password for a username"""
    start_time = perf_counter()
    
    username = username.strip()
    
    if not username:
        print(f"{Fore.RED}Error: Username cannot be empty!")
        return
    
    generated = f"{username}-{random.choice(config.WORDLIST)}-{random.randint(100,999)}*"
    
    if safe_file_write(config.USERS_FILE, f"{username} : {generated}\n"):
        msg = f"✓ Generated password: {generated}"
        print(f"{Fore.GREEN}{msg}")
        log_message("pass", msg)
        
        elapsed = (perf_counter() - start_time) * 1000
        log_message("pass", f"Command completed in {elapsed:.2f}ms")
    else:
        print(f"{Fore.RED}✗ Failed to save password")

def add_account(username, password):
    """Manually add an account to storage"""
    start_time = perf_counter()
    
    username = username.strip()
    password = password.strip()
    
    if not username or not password:
        print(f"{Fore.RED}Error: Username and password cannot be empty!")
        return
    
    if safe_file_write(config.USERS_FILE, f"{username} : {password}\n"):
        msg = f"✓ Added account '{username}'"
        print(f"{Fore.GREEN}{msg}")
        log_message("addacc", msg)
        
        elapsed = (perf_counter() - start_time) * 1000
        log_message("addacc", f"Command completed in {elapsed:.2f}ms")
    else:
        print(f"{Fore.RED}✗ Failed to add account")

def show_storage():
    """Display all saved accounts"""
    content = safe_file_read(config.USERS_FILE)
    
    if content is None or not content.strip():
        print(f"{Fore.YELLOW}No saved accounts found.")
    else:
        print(f"{Fore.CYAN}=== Saved Accounts ==={Style.RESET_ALL}\n")
        print(content)

def show_available():
    """Display all available usernames found"""
    content = safe_file_read(config.AVAILABLE_FILE)
    
    if content is None or not content.strip():
        print(f"{Fore.YELLOW}No available usernames found yet.")
        print(f"Run 'genkey' or 'check' commands to find available usernames.")
    else:
        print(f"{Fore.CYAN}=== Available Usernames ==={Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}{content}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Total found: {len(content.strip().split(chr(10)))}{Style.RESET_ALL}")

def show_settings():
    """Display current settings"""
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.YELLOW}           DuckSnipe Settings")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
    
    print(f"{Fore.MAGENTA}API Settings:{Style.RESET_ALL}")
    print(f"  Max Concurrent Requests: {Fore.GREEN}{config.MAX_CONCURRENT_REQUESTS}")
    print(f"  Request Delay (seconds): {Fore.GREEN}{config.REQUEST_DELAY}{Style.RESET_ALL}")
    
    print(f"\n{Fore.MAGENTA}File Paths:{Style.RESET_ALL}")
    print(f"  Log Folder: {Fore.CYAN}{config.LOG_FOLDER}")
    print(f"  Users File: {Fore.CYAN}{config.USERS_FILE}")
    print(f"  Words File: {Fore.CYAN}{config.WORDS_FILE}")
    print(f"  Available File: {Fore.CYAN}{config.AVAILABLE_FILE}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")

def modify_settings():
    """Interactive settings modification"""
    print(f"\n{Fore.CYAN}=== Modify Settings ==={Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}1. Max Concurrent Requests (currently: {config.MAX_CONCURRENT_REQUESTS})")
    print(f"2. Request Delay in seconds (currently: {config.REQUEST_DELAY})")
    print(f"3. Log Folder path (currently: {config.LOG_FOLDER})")
    print(f"4. Users File path (currently: {config.USERS_FILE})")
    print(f"5. Words File path (currently: {config.WORDS_FILE})")
    print(f"6. Available File path (currently: {config.AVAILABLE_FILE})")
    print(f"7. Reset to defaults")
    print(f"0. Back{Style.RESET_ALL}\n")
    
    choice = input(f"{Fore.CYAN}Select setting to modify (0-7): {Style.RESET_ALL}").strip()
    
    if choice == "1":
        try:
            new_val = int(input(f"{Fore.CYAN}Enter new Max Concurrent Requests (1-100): {Style.RESET_ALL}"))
            if 1 <= new_val <= 100:
                config.MAX_CONCURRENT_REQUESTS = new_val
                save_settings()
                print(f"{Fore.GREEN}✓ Updated Max Concurrent Requests to {new_val}")
            else:
                print(f"{Fore.RED}Error: Must be between 1 and 100!")
        except ValueError:
            print(f"{Fore.RED}Error: Invalid number!")
    
    elif choice == "2":
        try:
            new_val = float(input(f"{Fore.CYAN}Enter new Request Delay (0-10): {Style.RESET_ALL}"))
            if 0 <= new_val <= 10:
                config.REQUEST_DELAY = new_val
                save_settings()
                print(f"{Fore.GREEN}✓ Updated Request Delay to {new_val}s")
            else:
                print(f"{Fore.RED}Error: Must be between 0 and 10!")
        except ValueError:
            print(f"{Fore.RED}Error: Invalid number!")
    
    elif choice == "3":
        new_val = input(f"{Fore.CYAN}Enter new Log Folder path: {Style.RESET_ALL}").strip()
        if new_val:
            config.LOG_FOLDER = new_val
            save_settings()
            print(f"{Fore.GREEN}✓ Updated Log Folder to {new_val}")
    
    elif choice == "4":
        new_val = input(f"{Fore.CYAN}Enter new Users File path: {Style.RESET_ALL}").strip()
        if new_val:
            config.USERS_FILE = new_val
            save_settings()
            print(f"{Fore.GREEN}✓ Updated Users File to {new_val}")
    
    elif choice == "5":
        new_val = input(f"{Fore.CYAN}Enter new Words File path: {Style.RESET_ALL}").strip()
        if new_val:
            config.WORDS_FILE = new_val
            save_settings()
            print(f"{Fore.GREEN}✓ Updated Words File to {new_val}")
    
    elif choice == "6":
        new_val = input(f"{Fore.CYAN}Enter new Available File path: {Style.RESET_ALL}").strip()
        if new_val:
            config.AVAILABLE_FILE = new_val
            save_settings()
            print(f"{Fore.GREEN}✓ Updated Available File to {new_val}")
    
    elif choice == "7":
        confirm = input(f"{Fore.RED}Reset all settings to default? (y/n): {Style.RESET_ALL}").strip().lower()
        if confirm == 'y':
            config.MAX_CONCURRENT_REQUESTS = 10
            config.REQUEST_DELAY = 0.3
            config.LOG_FOLDER = "DuckSnipeLogs"
            config.USERS_FILE = "users.txt"
            config.WORDS_FILE = "words.txt"
            config.AVAILABLE_FILE = "available_usernames.txt"
            save_settings()
            print(f"{Fore.GREEN}✓ All settings reset to defaults!")
            print(f"{Fore.CYAN}  - Max Concurrent Requests: 10")
            print(f"{Fore.CYAN}  - Request Delay: 0.3s")

def show_commands():
    """Display all available commands"""
    print(f"""
{Fore.CYAN}=== DuckSnipe Commands ==={Style.RESET_ALL}

{Fore.YELLOW}genkey [type] [key]{Style.RESET_ALL}     - Generate & check usernames
                          Types: wordlist, studio, minerals, custom, great, jobs

{Fore.YELLOW}letter_gen{Style.RESET_ALL}              - Generate random letter usernames (interactive)
                          
{Fore.YELLOW}check [username]{Style.RESET_ALL}        - Check if a username is available

{Fore.YELLOW}available{Style.RESET_ALL}               - View all available usernames found

{Fore.YELLOW}settings{Style.RESET_ALL}                - View and modify settings

{Fore.YELLOW}addword [word]{Style.RESET_ALL}          - Add a custom word to your wordlist

{Fore.YELLOW}pass [username]{Style.RESET_ALL}         - Generate a random password for username

{Fore.YELLOW}addacc [user] [pass]{Style.RESET_ALL}    - Manually save an account

{Fore.YELLOW}storage{Style.RESET_ALL}                 - Show all saved accounts

{Fore.YELLOW}cmds{Style.RESET_ALL}                    - Show this command list

{Fore.YELLOW}help{Style.RESET_ALL}                    - Show detailed help guide

{Fore.YELLOW}clear{Style.RESET_ALL}                   - Clear available snipes list (in memory only)

{Fore.YELLOW}exit/quit{Style.RESET_ALL}               - Exit DuckSnipe

{Fore.CYAN}========================{Style.RESET_ALL}
""")

def show_help():
    """Display detailed help information"""
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════╗
║       DuckSnipe v{config.VERSION} - Help       ║
╚═══════════════════════════════════════╝{Style.RESET_ALL}

{Fore.YELLOW}COMMANDS:{Style.RESET_ALL}
---------
{Fore.GREEN}genkey [type] [key]{Style.RESET_ALL}
  Generate username combinations and check availability
  
  Types available:
    - wordlist  : Common words
    - studio    : Roblox Studio terms
    - minerals  : Mineral/element names
    - custom    : Your custom words (add with 'addword')
    - great     : Premium Roblox-related words
    - jobs      : Job/profession names
  
  Example: genkey wordlist Pro

{Fore.GREEN}letter_gen{Style.RESET_ALL}
  Generate random letter-based usernames
  Interactive prompts for length, count (1-50000 or 'max'), and numbers
  
  Example: letter_gen

{Fore.GREEN}settings{Style.RESET_ALL}
  View and modify application settings:
    - API rate limiting (concurrent requests, delays)
    - File paths (logs, users, words, available)
    - Reset to defaults

{Fore.GREEN}check [username1] [username2] ...{Style.RESET_ALL}
  Check specific usernames for availability
  
{Fore.GREEN}available{Style.RESET_ALL}
  View all available usernames found

{Fore.YELLOW}FEATURES:{Style.RESET_ALL}
---------
• Concurrent username checking (fast!)
• Automatic logging to {config.LOG_FOLDER}/
• Available usernames saved to {config.AVAILABLE_FILE}
• Customizable settings
• Color-coded output
• Rate limit detection

Press Enter to continue...
""")
    input()

def clear_snipes():
    """Clear the available snipes list"""
    count = len(config.AVAILABLE_SNIPES)
    config.AVAILABLE_SNIPES.clear()
    print(f"{Fore.GREEN}✓ Cleared {count} available snipes from memory")
    print(f"{Fore.YELLOW}Note: {config.AVAILABLE_FILE} is not affected")

async def handle_genkey(args):
    """Handle genkey command"""
    start_time = perf_counter()
    
    if len(args) < 2:
        print(f"{Fore.RED}Error: Missing arguments!")
        print(f"{Fore.YELLOW}Usage: genkey [type] [key]")
        print(f"Types: wordlist, studio, minerals, custom, great, jobs")
        return
    
    key_type, key_val = args[0].lower(), args[1]
    
    sources = {
        "wordlist": config.WORDLIST,
        "studio": config.RBXSTUDIO,
        "minerals": config.MINERALS,
        "custom": config.CUSTOM_WORDS,
        "great": config.GREATNAME,
        "jobs": config.JOBLIST
    }
    
    if key_type not in sources:
        print(f"{Fore.RED}Error: Unknown type '{key_type}'")
        print(f"{Fore.YELLOW}Available types: {', '.join(sources.keys())}")
        return
    
    source = sources[key_type]
    
    if not source:
        print(f"{Fore.RED}Error: '{key_type}' wordlist is empty!")
        if key_type == "custom":
            print(f"{Fore.YELLOW}Add words with: addword [word]")
        return
    
    usernames = []
    for word in source:
        usernames.append(f"{key_val}{word}")
        usernames.append(f"{word}{key_val}")
    
    msg = f"Generated {len(usernames)} usernames from '{key_type}' with key '{key_val}'"
    print(f"{Fore.CYAN}{msg}")
    log_message("genkey", msg)
    
    await validate_usernames_concurrent(usernames, "genkey")
    
    elapsed = (perf_counter() - start_time) * 1000
    log_message("genkey", f"Command completed in {elapsed:.2f}ms")

async def handle_check(args):
    """Handle check command"""
    start_time = perf_counter()
    
    if not args:
        print(f"{Fore.RED}Error: No usernames provided!")
        print(f"{Fore.YELLOW}Usage: check [username1] [username2] ...")
        return
    
    await validate_usernames_concurrent(args, "check")
    
    elapsed = (perf_counter() - start_time) * 1000
    log_message("check", f"Command completed in {elapsed:.2f}ms")

def generate_random_username(length, include_numbers):
    """Generate a random username with specified length"""
    if include_numbers:
        chars = string.ascii_letters + string.digits
    else:
        chars = string.ascii_letters
    
    username = random.choice(string.ascii_letters)
    username += ''.join(random.choices(chars, k=length - 1))
    
    return username

async def handle_letter_gen():
    """Handle letter_gen command - interactive username generator"""
    start_time = perf_counter()
    
    print(f"\n{Fore.CYAN}=== Random Username Generator ==={Style.RESET_ALL}\n")
    
    while True:
        try:
            length_input = input(f"{Fore.YELLOW}Enter number of characters (3-20): {Style.RESET_ALL}").strip()
            length = int(length_input)
            if 3 <= length <= 20:
                break
            else:
                print(f"{Fore.RED}Error: Length must be between 3 and 20!")
        except ValueError:
            print(f"{Fore.RED}Error: Please enter a valid number!")
    
    while True:
        try:
            count_input = input(f"{Fore.YELLOW}How many usernames to generate? (1-50000 or 'max'): {Style.RESET_ALL}").strip().lower()
            
            if count_input == 'max' or count_input == 'maximum':
                if length <= 3:
                    max_combinations = 26 ** length
                else:
                    max_combinations = (26 + 10) ** length
                
                count = min(max_combinations, 50000)
                print(f"{Fore.CYAN}Generating maximum: {count} usernames")
                break
            else:
                count = int(count_input)
                if 1 <= count <= 50000:
                    break
                else:
                    print(f"{Fore.RED}Error: Count must be between 1 and 50000!")
        except ValueError:
            print(f"{Fore.RED}Error: Please enter a valid number or 'max'!")
    
    while True:
        include_input = input(f"{Fore.YELLOW}Include numbers? (y/n): {Style.RESET_ALL}").strip().lower()
        if include_input in ['y', 'yes']:
            include_numbers = True
            break
        elif include_input in ['n', 'no']:
            include_numbers = False
            break
        else:
            print(f"{Fore.RED}Error: Please enter 'y' or 'n'!")
    
    print(f"\n{Fore.CYAN}Generating {count} random {length}-character usernames...")
    usernames = set()
    
    max_attempts = count * 3
    attempts = 0
    
    while len(usernames) < count and attempts < max_attempts:
        username = generate_random_username(length, include_numbers)
        usernames.add(username)
        attempts += 1
    
    usernames = list(usernames)
    
    if len(usernames) < count:
        print(f"{Fore.YELLOW}Note: Generated {len(usernames)} unique usernames (requested {count})")
    
    msg = f"Generated {len(usernames)} random usernames (length: {length}, numbers: {include_numbers})"
    print(f"{Fore.CYAN}{msg}")
    log_message("letter_gen", msg)
    
    await validate_usernames_concurrent(usernames, "letter_gen")
    
    elapsed = (perf_counter() - start_time) * 1000
    log_message("letter_gen", f"Command completed in {elapsed:.2f}ms")