import random
import os
import time
import asyncio
import aiohttp
import re
from datetime import datetime
from time import perf_counter
from colorama import init, Fore, Back, Style

# ---------------- Constants ---------------- #
VERSION = "1.0.8"
WORDLIST = ["verified","public","sound","un","war","star","course","glitch","private","secure",
"taste","test","taken","build","bought","tower","script","house","sky","building","bank","demo",
"gun","money","vampire","lua","code","dirt","stone","rock","sand","water","lava","fire","brick",
"badge","guest","copper","tree","wire","light","thunder","rain","word","blood","duck","snipe",
"rifle","god","angel","internet","google","guilded","web","hunt","cute","skull","legal","mc",
"wild","crazy","bin","ban","banned","banish","og","roblox","epic","tix","module","local","bot",
"secret","weapon","storage","wish","wind","whole","plays","forest","sub","leave",
"add","age","air","and","any","art","ash","bad","bar","base","bath","be","beat","bed","bell",
"best","bit","black","blue","board","box","boy","bug","call","camp","cap","car","card","cat",
"cell","chat","chip","city","clan","clip","club","coal","cold","copy","core","cost","cow",
"craft","cross","dark","data","day","deal","desk","dig","disk","dog","door","dot","drop","dust",
"edit","egg","end","evil","eye","fall","farm","fast","file","find","fish","flag","flow","fly",
"food","foot","free","frog","game","gas","gate","gift","gold","grab","grass","green","grid",
"grow","hack","hand","hard","hat","head","heat","help","hit","hold","home","hope","host","ice",
"id","item","join","jump","key","kill","king","kit","lake","lamp","land","last","law","lead",
"leaf","left","life","link","list","load","lock","log","lost","low","map","mark","mask","math",
"meat","menu","milk","mine","mode","moon","move","name","net","new","night","node","note","npc",
"open","page","path","pay","pet","pick","ping","pipe","play","pool","post","power","press",
"price","print","quest","quick","rank","read","real","red","rest","ride","ring","road","role",
"room","root","rule","run","safe","save","scan","seed","sell","send","set","shop","shot","show",
"sign","skin","sleep","slot","slow","snow","soft","song","sort","spam","spin","spot","stack",
"staff","stage","stand","start","steam","step","stick","stop","storm","swap","talk","tank",
"task","team","tech","text","tick","time","tip","tool","top","trade","trap","true",
"type","unit","use","user","value","view","void","vote","walk","wall","watch","wave","way",
"win","wood","work","world","xp","zone"]


MINERALS = ["dirt","stone","rock","sand","water","lava","fire","copper","rain","ruby","diamond"]
RBXSTUDIO = ["model","mesh","part","audio","tool","decal","animation","collider","constraint",
"controller","emitter","keyframe","material","node","physics","render","terrain","texture","UI",
"workspace","vector","algorithm","array","boolean","buffer","class","compiler","coroutine","debug",
"enum","iterator","method","namespace","parameter","recursive","stack","variable"]

GREATNAME = ["roblox","hex","mod","telamon","builderman","tix","diamond","epic"]
JOBLIST = ["artist","engineer","worker","painter","programmer","coder","teacher","musician","lawyer"]

LOWER = [
    'a','b','c','d','e','f','g','h','i','j',
    'k','l','m','n','o','p','q','r','s','t',
    'u','v','w','x','y','z'
]
CHARS = [
    'a','b','c','d','e','f','g','h','i','j',
    'k','l','m','n','o','p','q','r','s','t',
    'u','v','w','x','y','z',
    '0','1','2','3','4','5','6','7','8','9'
]


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
                0: f"{Fore.GREEN}✓ {username} is available!{Style.RESET_ALL}",
                1: f"{Fore.RED}✗ {username} is taken.{Style.RESET_ALL}",
                2: f"{Fore.RED}✗ {username} is inappropriate.{Style.RESET_ALL}",
                10: f"{Fore.RED}✗ {username} may contain private info.{Style.RESET_ALL}"
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
    print(f"""
{Fore.CYAN}=== DuckSnipe Commands ==={Style.RESET_ALL}

genkey [type] [key]     {Fore.YELLOW}- Generate & check usernames
                          Types: wordlist, studio, minerals, custom, great, jobs{Style.RESET_ALL}
          
gen [type] [att]        {Fore.YELLOW}- Generate & check usernames based off a list of generators.
                          Types: 4l, 4char, 5l, 5char, 6l, 6char{Style.RESET_ALL}

gennum [length] [att]   {Fore.YELLOW}- Generate & check number usernames based off a digit length.{Style.RESET_ALL}

genother [type] [key]   {Fore.YELLOW}- Generate & check usernames based on misc gens
                          Types: key##, key#{Style.RESET_ALL}
                          
check [username]        {Fore.YELLOW}- Check if a username is available{Style.RESET_ALL}

addword [word]          {Fore.YELLOW}- Add a custom word to your wordlist{Style.RESET_ALL}

pass [username]         {Fore.YELLOW}- Generate a random password for username{Style.RESET_ALL}

addacc [user] [pass]    {Fore.YELLOW}- Manually save an account{Style.RESET_ALL}

storage                 {Fore.YELLOW}- Show all saved accounts{Style.RESET_ALL}

cmds                    {Fore.YELLOW}- Show this command list{Style.RESET_ALL}

help                    {Fore.YELLOW}- Show detailed help guide{Style.RESET_ALL}

clearsnipes             {Fore.YELLOW}- Clear available snipes list{Style.RESET_ALL}

clear                   {Fore.YELLOW}- Clear the screen/terminal{Style.RESET_ALL}

exit/quit               {Fore.YELLOW}- Exit DuckSnipe{Style.RESET_ALL}

{Fore.CYAN}========================{Style.RESET_ALL}
""")

def show_help():
    """Display detailed help information"""
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════╗
║       DuckSnipe v{VERSION} - Help       ║
╚═══════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}COMMANDS:{Style.RESET_ALL}
---------
{Fore.BLUE}genkey [type] [key]{Style.RESET_ALL}
  Generate username combinations and check availability
  
  Types available:
    - wordlist  : Common words
    - studio    : Roblox Studio terms
    - minerals  : Mineral/element names
    - custom    : Your custom words (add with 'addword')
    - great     : Premium Roblox-related words
    - jobs      : Job/profession names
  
  {Fore.MAGENTA}Example: genkey wordlist Pro
           (checks: Proverified, verifiedPro, Propublic, etc.){Style.RESET_ALL}

{Fore.BLUE}gen [type] [attempts]{Style.RESET_ALL}
  Generate usernames based off a generator and check availability
  
  Types available:
    - wordlist  : Common words
    - 4l        : 4 letter usernames
    - 4char     : 4 character usernames (with numbers)
    - 5l        : 5 letter usernames
    - 5char     : 5 character usernames (with numbers)
    - 6l        : 6 letter usernames
    - 6char     : 6 character usernames (with numbers)

{Fore.BLUE}gennum [length] [attempts]{Style.RESET_ALL}
  Generate number usernames based off digit length and check availability
  
  {Fore.MAGENTA}Example: gennum 5 100
           (checks: 32245, 81676, 89273, etc.){Style.RESET_ALL}

{Fore.BLUE}genother [type] [key]{Style.RESET_ALL}
  Generate username combinations and check availability based on misc gens
  
  Types available:
    - key##     : Key + two numbers
    - key#      : Key + one number
  
  {Fore.MAGENTA}Example: genother key## bob
           (checks: bob10, bob11, bob12, etc.){Style.RESET_ALL}

{Fore.BLUE}check [username1] [username2] ...{Style.RESET_ALL}
  Check specific usernames for availability
  
  {Fore.MAGENTA}Example: check CoolDude123 EpicGamer456{Style.RESET_ALL}

{Fore.BLUE}addword [word]{Style.RESET_ALL}
  Add a word to your custom wordlist
  
  {Fore.MAGENTA}Example: addword ninja{Style.RESET_ALL}

{Fore.BLUE}pass [username]{Style.RESET_ALL}
  Generate and save a random password
  
  {Fore.MAGENTA}Example: pass CoolDude123{Style.RESET_ALL}

{Fore.BLUE}addacc [username] [password]{Style.RESET_ALL}
  Manually save account credentials
  
  {Fore.MAGENTA}Example: addacc CoolDude123 MyPassword123{Style.RESET_ALL}

{Fore.BLUE}storage{Style.RESET_ALL}
  View all saved account credentials

{Fore.BLUE}clearsnipes{Style.RESET_ALL}
  Clear the list of available snipes found in current session

{Fore.BLUE}clr{Style.RESET_ALL}
  Clear the screen/terminal

{Fore.GREEN}FEATURES:{Style.RESET_ALL}
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

async def handle_gen(args):
    """Handle gen command"""
    start_time = perf_counter()
    
    if len(args) < 2:
        print("Error: Missing arguments!")
        print("Usage: genkey [type] [attempts]")
        print("Types: 4l, 4char, 5l, 5char, 6l, 6char")
        return
    
    gen_type, gen_attempts = args[0].lower(), args[1]
    
    gens = {
        "4l",
        "4char",
        "5l",
        "5char",
        "6l",
        "6char"
    }
    
    if gen_type not in gens:
        print(f"Error: Unknown type '{gen_type}'")
        print(f"Available generator types: {', '.join(gens.keys())}")
        return
    elif not gen_attempts.isdigit():
        print(f"Error: Please use a valid number for the attempts.")
        return
    
    usernames = []
    if gen_type == "4l":
        for l4 in range(int(gen_attempts)):
            usernames.append(random.choice(LOWER) + random.choice(LOWER) + random.choice(LOWER) + random.choice(LOWER))
    elif gen_type == "4char":
        for l4 in range(int(gen_attempts)):
            usernames.append(random.choice(CHARS) + random.choice(CHARS) + random.choice(CHARS) + random.choice(CHARS))
    elif gen_type == "5l":
        for l5 in range(int(gen_attempts)):
            usernames.append(random.choice(LOWER) + random.choice(LOWER) + random.choice(LOWER) + random.choice(LOWER) + random.choice(LOWER))
    elif gen_type == "5char":
        for l5 in range(int(gen_attempts)):
            usernames.append(random.choice(CHARS) + random.choice(CHARS) + random.choice(CHARS) + random.choice(CHARS) + random.choice(CHARS))
    elif gen_type == "6l":
        for l6 in range(int(gen_attempts)):
            usernames.append(random.choice(LOWER) + random.choice(LOWER) + random.choice(LOWER) + random.choice(LOWER) + random.choice(LOWER) + random.choice(LOWER))
    elif gen_type == "6char":
        for l6 in range(int(gen_attempts)):
            usernames.append(random.choice(CHARS) + random.choice(CHARS) + random.choice(CHARS) + random.choice(CHARS) + random.choice(CHARS) + random.choice(CHARS))
    
    msg = f"Generated {len(usernames)} usernames from '{gen_type}' with {gen_attempts} attempts"
    print(msg)
    log_message("gen", msg)
    
    await validate_usernames_concurrent(usernames, "gen")
    
    elapsed = (perf_counter() - start_time) * 1000
    log_message("gen", f"Command completed in {elapsed:.2f}ms")

async def handle_gennum(args):
    """Handle gennum command"""
    start_time = perf_counter()
    
    if len(args) < 2:
        print("Error: Missing arguments!")
        print("Usage: gennum [length] [attempts]")
        return
    
    gen_length, gen_attempts = args[0], args[1]
    
    if not gen_length.isdigit():
        print(f"Error: Please use a valid number for the length.")
        return
    elif not gen_attempts.isdigit():
        print(f"Error: Please use a valid number for the attempts.")
        return
    
    usernames = []
    lengthmin, lengthmax = 10 ** (int(gen_length) - 1), 10 ** int(gen_length)
    for att in range(int(gen_attempts)):
        usernames.append(str(random.randint(lengthmin,lengthmax)))
    
    msg = f"Generated {len(usernames)} usernames with number length of {gen_length} with {gen_attempts} attempts"
    print(msg)
    log_message("gennum", msg)
    
    await validate_usernames_concurrent(usernames, "gennum")
    
    elapsed = (perf_counter() - start_time) * 1000
    log_message("gennum", f"Command completed in {elapsed:.2f}ms")

async def handle_genother(args):
    """Handle genother command"""
    start_time = perf_counter()
    
    if len(args) < 2:
        print("Error: Missing arguments!")
        print("Usage: genother [type] [key]")
        print("Available Types: key##, key#")
        return
    
    otherGenerators = [
        "key##",
        "key#",
    ]

    key_type, key_val = args[0].lower(), args[1]

    if key_type not in otherGenerators:
        print(f"Error: Generator Type '{key_type}' does not exist")
        print("Available Types: key##, key#")
        return
    
    usernames = []
    if key_type == "key##":
        for k2_one in range(10,100):
            usernames.append(key_val + str(k2_one))
        for k2_one in range(10,100):
            usernames.append(str(k2_one) + key_val)
    elif key_type == "key#":
        for k2_one in range(0,10):
            usernames.append(key_val + str(k2_one))
        for k2_one in range(0,10):
            usernames.append(str(k2_one) + key_val)

    msg = f"Generated {len(usernames)} usernames using '{key_type}' with key '{key_val}'"
    print(msg)
    log_message("genother", msg)
    
    await validate_usernames_concurrent(usernames, "genother")
    
    elapsed = (perf_counter() - start_time) * 1000
    log_message("genother", f"Command completed in {elapsed:.2f}ms")

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
{Fore.CYAN}╔═══════════════════════════════════════╗
║     DuckSnipe v{VERSION} Started      ║
╚═══════════════════════════════════════╝{Style.RESET_ALL}

Type 'help' for guide or 'cmds' for command list
""")
    
    while True:
        try:
            cmd_input = input(Fore.CYAN + "\n==> " + Style.RESET_ALL).strip()
            
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
                
            elif cmd == "clearsnipes":
                clear_snipes()

            elif cmd == "clr":
                clear_screen()
            
            # Handle async commands
            elif cmd == "genkey":
                asyncio.run(handle_genkey(args))
                input("\nPress Enter to continue...")
            
            elif cmd == "gen":
                asyncio.run(handle_gen(args))
                input("\nPress Enter to continue...")

            elif cmd == "gennum":
                asyncio.run(handle_gennum(args))
                input("\nPress Enter to continue...")
            
            elif cmd == "genother":
                asyncio.run(handle_genother(args))
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
