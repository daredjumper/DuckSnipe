"""
DuckSnipe Commands
All command implementations and handlers
"""

import random
import asyncio
from time import perf_counter
from config import (VERSION, WORDLIST, RBXSTUDIO, MINERALS, GREATNAME, JOBLIST,
                    CUSTOM_WORDS, AVAILABLE_SNIPES, USERS_FILE, WORDS_FILE, 
                    LOG_FOLDER, AVAILABLE_FILE)
from utils import safe_file_write, safe_file_read, log_message, sync_custom_words
from api import validate_usernames_concurrent

def add_word(word):
    """Add a custom word to the wordlist"""
    start_time = perf_counter()
    
    word = word.strip()
    
    if not word:
        print("Error: Word cannot be empty!")
        return
    
    if word in CUSTOM_WORDS:
        print(f"'{word}' is already in custom words!")
        return
    
    if safe_file_write(WORDS_FILE, f"{word},"):
        sync_custom_words()
        msg = f"✓ Added word '{word}' to custom wordlist"
        print(msg)
        log_message("addword", msg)
        
        elapsed = (perf_counter() - start_time) * 1000
        log_message("addword", f"Command completed in {elapsed:.2f}ms")
    else:
        print("✗ Failed to add word")

def generate_pass(username):
    """Generate a random password for a username"""
    start_time = perf_counter()
    
    username = username.strip()
    
    if not username:
        print("Error: Username cannot be empty!")
        return
    
    generated = f"{username}-{random.choice(WORDLIST)}-{random.randint(100,999)}*"
    
    if safe_file_write(USERS_FILE, f"{username} : {generated}\n"):
        msg = f"✓ Generated password: {generated}"
        print(msg)
        log_message("pass", msg)
        
        elapsed = (perf_counter() - start_time) * 1000
        log_message("pass", f"Command completed in {elapsed:.2f}ms")
    else:
        print("✗ Failed to save password")

def add_account(username, password):
    """Manually add an account to storage"""
    start_time = perf_counter()
    
    username = username.strip()
    password = password.strip()
    
    if not username or not password:
        print("Error: Username and password cannot be empty!")
        return
    
    if safe_file_write(USERS_FILE, f"{username} : {password}\n"):
        msg = f"✓ Added account '{username}'"
        print(msg)
        log_message("addacc", msg)
        
        elapsed = (perf_counter() - start_time) * 1000
        log_message("addacc", f"Command completed in {elapsed:.2f}ms")
    else:
        print("✗ Failed to add account")

def show_storage():
    """Display all saved accounts"""
    content = safe_file_read(USERS_FILE)
    
    if content is None or not content.strip():
        print("No saved accounts found.")
    else:
        print("=== Saved Accounts ===\n")
        print(content)

def show_available():
    """Display all available usernames found"""
    content = safe_file_read(AVAILABLE_FILE)
    
    if content is None or not content.strip():
        print("No available usernames found yet.")
        print(f"Run 'genkey' or 'check' commands to find available usernames.")
    else:
        print("=== Available Usernames ===\n")
        print(content)
        print(f"\nTotal found: {len(content.strip().split(chr(10)))}")

def show_commands():
    """Display all available commands"""
    print("""
=== DuckSnipe Commands ===

genkey [type] [key]     - Generate & check usernames
                          Types: wordlist, studio, minerals, custom, great, jobs
                          
check [username]        - Check if a username is available

available               - View all available usernames found

addword [word]          - Add a custom word to your wordlist

pass [username]         - Generate a random password for username

addacc [user] [pass]    - Manually save an account

storage                 - Show all saved accounts

cmds                    - Show this command list

help                    - Show detailed help guide

clear                   - Clear available snipes list (in memory only)

exit/quit               - Exit DuckSnipe

========================
""")

def show_help():
    """Display detailed help information"""
    print(f"""
╔═══════════════════════════════════════╗
║       DuckSnipe v{VERSION} - Help       ║
╚═══════════════════════════════════════╝

COMMANDS:
---------
genkey [type] [key]
  Generate username combinations and check availability
  
  Types available:
    - wordlist  : Common words
    - studio    : Roblox Studio terms
    - minerals  : Mineral/element names
    - custom    : Your custom words (add with 'addword')
    - great     : Premium Roblox-related words
    - jobs      : Job/profession names
  
  Example: genkey wordlist Pro
           (checks: Proverified, verifiedPro, Propublic, etc.)

check [username1] [username2] ...
  Check specific usernames for availability
  
  Example: check CoolDude123 EpicGamer456

available
  View all available usernames found
  These are automatically saved to {AVAILABLE_FILE}

addword [word]
  Add a word to your custom wordlist
  
  Example: addword ninja

pass [username]
  Generate and save a random password
  
  Example: pass CoolDude123

addacc [username] [password]
  Manually save account credentials
  
  Example: addacc CoolDude123 MyPassword123

storage
  View all saved account credentials

clear
  Clear the list of available snipes from memory
  (does not delete from {AVAILABLE_FILE})

FEATURES:
---------
• Concurrent username checking (fast!)
• Automatic logging to {LOG_FOLDER}/
• Available usernames saved to {AVAILABLE_FILE}
• Password generation
• Custom wordlist support
• Account storage

Press Enter to continue...
""")
    input()

def clear_snipes():
    """Clear the available snipes list"""
    count = len(AVAILABLE_SNIPES)
    AVAILABLE_SNIPES.clear()
    print(f"✓ Cleared {count} available snipes from memory")
    print(f"Note: {AVAILABLE_FILE} is not affected")

async def handle_genkey(args):
    """Handle genkey command"""
    start_time = perf_counter()
    
    if len(args) < 2:
        print("Error: Missing arguments!")
        print("Usage: genkey [type] [key]")
        print("Types: wordlist, studio, minerals, custom, great, jobs")
        return
    
    key_type, key_val = args[0].lower(), args[1]
    
    sources = {
        "wordlist": WORDLIST,
        "studio": RBXSTUDIO,
        "minerals": MINERALS,
        "custom": CUSTOM_WORDS,
        "great": GREATNAME,
        "jobs": JOBLIST
    }
    
    if key_type not in sources:
        print(f"Error: Unknown type '{key_type}'")
        print(f"Available types: {', '.join(sources.keys())}")
        return
    
    source = sources[key_type]
    
    if not source:
        print(f"Error: '{key_type}' wordlist is empty!")
        if key_type == "custom":
            print("Add words with: addword [word]")
        return
    
    usernames = []
    for word in source:
        usernames.append(f"{key_val}{word}")
        usernames.append(f"{word}{key_val}")
    
    msg = f"Generated {len(usernames)} usernames from '{key_type}' with key '{key_val}'"
    print(msg)
    log_message("genkey", msg)
    
    await validate_usernames_concurrent(usernames, "genkey")
    
    elapsed = (perf_counter() - start_time) * 1000
    log_message("genkey", f"Command completed in {elapsed:.2f}ms")

async def handle_check(args):
    """Handle check command"""
    start_time = perf_counter()
    
    if not args:
        print("Error: No usernames provided!")
        print("Usage: check [username1] [username2] ...")
        return
    
    await validate_usernames_concurrent(args, "check")
    
    elapsed = (perf_counter() - start_time) * 1000
    log_message("check", f"Command completed in {elapsed:.2f}ms")