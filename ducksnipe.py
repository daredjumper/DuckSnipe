import random
import os
import time
import asyncio
import aiohttp
import re
from datetime import datetime
from time import perf_counter

# ---------------- Constants ---------------- #
VERSION = "1.0.8"
WORDLIST = ["verified","public","sound","un","war","star","course","glitch","private","secure",
"taste","test","taken","build","bought","tower","script","house","sky","building","bank","demo",
"gun","money","vampire","lua","code","dirt","stone","rock","sand","water","lava","fire","brick",
"badge","guest","copper","tree","wire","light","thunder","rain","word","blood","duck","snipe",
"rifle","god","angel","internet","google","guilded","web","hunt","cute","skull","legal","mc",
"wild","crazy","bin","ban","banned","banish","og","roblox","epic","tix","module","local","bot",
"secret","weapon","storage","wish","wind","whole","plays","forest","sub","leave"]

MINERALS = ["dirt","stone","rock","sand","water","lava","fire","copper","rain","ruby","diamond"]
RBXSTUDIO = ["model","mesh","part","audio","tool","decal","animation","collider","constraint",
"controller","emitter","keyframe","material","node","physics","render","terrain","texture","UI",
"workspace","vector","algorithm","array","boolean","buffer","class","compiler","coroutine","debug",
"enum","iterator","method","namespace","parameter","recursive","stack","variable"]

GREATNAME = ["roblox","hex","mod","telamon","builderman","tix","diamond","epic"]
JOBLIST = ["artist","engineer","worker","painter","programmer","coder","teacher","musician","lawyer"]

AVAILABLE_SNIPES = []
CUSTOM_WORDS = []

LOG_FOLDER = "DuckSnipeLogs"
USERS_FILE = "users.txt"
WORDS_FILE = "words.txt"

# ---------------- Initialization ---------------- #
os.makedirs(LOG_FOLDER, exist_ok=True)

# ---------------- Utility ---------------- #
def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def sync_custom_words():
    """Load custom words from file"""
    global CUSTOM_WORDS
    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            CUSTOM_WORDS = [w.strip() for w in content.split(",") if w.strip()]
    except FileNotFoundError:
        CUSTOM_WORDS = []
        # Create empty file
        with open(WORDS_FILE, "w", encoding="utf-8") as f:
            pass

def log_message(command_name, text):
    """Strip ANSI color codes and append to log file"""
    plain = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = os.path.join(LOG_FOLDER, f"{command_name}_output.txt")
    
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {plain}\n")
    except Exception as e:
        print(f"Warning: Could not write to log: {e}")

def safe_file_write(filepath, content, mode="a"):
    """Safely write to file with error handling"""
    try:
        with open(filepath, mode, encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing to {filepath}: {e}")
        return False

def safe_file_read(filepath):
    """Safely read from file with error handling"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

# ---------------- Async API ---------------- #
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

# ---------------- Commands ---------------- #
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
    
    # Append with comma
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

def show_commands():
    """Display all available commands"""
    print("""
=== DuckSnipe Commands ===

genkey [type] [key]     - Generate & check usernames
                          Types: wordlist, studio, minerals, custom, great, jobs
                          
check [username]        - Check if a username is available

addword [word]          - Add a custom word to your wordlist

pass [username]         - Generate a random password for username

addacc [user] [pass]    - Manually save an account

storage                 - Show all saved accounts

cmds                    - Show this command list

help                    - Show detailed help guide

clear                   - Clear available snipes list

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
  Clear the list of available snipes found in current session

FEATURES:
---------
• Concurrent username checking (fast!)
• Automatic logging to {LOG_FOLDER}/
• Password generation
• Custom wordlist support
• Account storage

Press Enter to continue...
""")
    input()

def clear_snipes():
    """Clear the available snipes list"""
    global AVAILABLE_SNIPES
    count = len(AVAILABLE_SNIPES)
    AVAILABLE_SNIPES = []
    print(f"✓ Cleared {count} available snipes from memory")

# ---------------- Command Handlers ---------------- #
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

# ---------------- Main Loop ---------------- #
def main():
    """Main application loop"""
    sync_custom_words()
    
    print(f"""
╔═══════════════════════════════════════╗
║     DuckSnipe v{VERSION} Started      ║
╚═══════════════════════════════════════╝

Type 'help' for guide or 'cmds' for command list
""")
    
    while True:
        try:
            cmd_input = input("\n==> ").strip()
            
            if not cmd_input:
                continue
            
            parts = cmd_input.split()
            cmd = parts[0].lower()
            args = parts[1:]
            
            # Handle exit commands
            if cmd in ["exit", "quit"]:
                print("Thanks for using DuckSnipe! Goodbye.")
                break
            
            # Handle sync commands
            elif cmd == "cmds":
                show_commands()
                
            elif cmd == "help":
                show_help()
                
            elif cmd == "addword":
                if args:
                    add_word(args[0])
                else:
                    print("Usage: addword [word]")
                    
            elif cmd == "pass":
                if args:
                    generate_pass(args[0])
                else:
                    print("Usage: pass [username]")
                    
            elif cmd == "addacc":
                if len(args) >= 2:
                    add_account(args[0], args[1])
                else:
                    print("Usage: addacc [username] [password]")
                    
            elif cmd == "storage":
                show_storage()
                input("\nPress Enter to continue...")
                
            elif cmd == "clear":
                clear_snipes()
            
            # Handle async commands
            elif cmd == "genkey":
                asyncio.run(handle_genkey(args))
                input("\nPress Enter to continue...")
                
            elif cmd == "check":
                asyncio.run(handle_check(args))
                input("\nPress Enter to continue...")
                
            else:
                print(f"Unknown command: '{cmd}'")
                print("Type 'help' for assistance or 'cmds' for command list")
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'exit' to quit.")
        except Exception as e:
            print(f"Error: {e}")
            log_message("error", f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
