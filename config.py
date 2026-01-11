"""
DuckSnipe Configuration
Contains all constants and wordlists
"""

VERSION = "1.0.8"

# Wordlists
WORDLIST = [
    "verified","public","sound","un","war","star","course","glitch","private","secure",
    "taste","test","taken","build","bought","tower","script","house","sky","building","bank","demo",
    "gun","money","vampire","lua","code","dirt","stone","rock","sand","water","lava","fire","brick",
    "badge","guest","copper","tree","wire","light","thunder","rain","word","blood","duck","snipe",
    "rifle","god","angel","internet","google","guilded","web","hunt","cute","skull","legal","mc",
    "wild","crazy","bin","ban","banned","banish","og","roblox","epic","tix","module","local","bot",
    "secret","weapon","storage","wish","wind","whole","plays","forest","sub","leave",
    
    # 200 Additional Words
    "pro","noob","elite","legend","master","king","queen","lord","boss","chief","ace","top",
    "mega","ultra","super","hyper","alpha","beta","omega","prime","max","ultimate","extreme",
    "shadow","dark","ghost","phantom","void","chaos","rage","fury","venom","toxic","savage",
    "dragon","phoenix","wolf","tiger","lion","eagle","hawk","viper","cobra","shark","beast",
    "blade","sword","axe","arrow","bolt","slash","strike","crush","blast","storm","thunder",
    "cyber","digital","pixel","byte","hack","tech","net","matrix","core","nexus","node",
    "run","dash","rush","speed","swift","quick","fast","zoom","fly","battle","combat","duel",
    "vip","premium","royal","grand","supreme","divine","rare","unique","special","limited",
    "neo","rex","kai","sky","fox","ice","zen","arc","lux","nova","volt","blaze","cruz",
    "red","blue","gold","silver","black","white","crimson","azure","emerald","obsidian",
    "neon","laser","plasma","atomic","quantum","cosmic","turbo","nitro","boost","power",
    "ninja","samurai","warrior","knight","mage","wizard","ranger","hunter","assassin","reaper",
    "flame","frost","volt","surge","pulse","wave","shock","burn","chill","freeze","melt",
    "steel","iron","bronze","titanium","chrome","crystal","diamond","ruby","sapphire","jade",
    "night","dawn","dusk","moon","solar","lunar","star","comet","meteor","galaxy","nebula",
    "rage","wrath","pride","envy","greed","chaos","order","balance","fate","doom","curse",
    "toxic","venom","poison","acid","plague","virus","infected","corrupted","tainted","cursed",
    "sniper","scout","tank","heavy","medic","support","carry","feeder","clutch","tryhard",
    "swag","drip","flex","vibe","mood","lit","fire","heat","goat","chad","sigma","based"
]

MINERALS = ["dirt","stone","rock","sand","water","lava","fire","copper","rain","ruby","diamond"]

RBXSTUDIO = ["model","mesh","part","audio","tool","decal","animation","collider","constraint",
"controller","emitter","keyframe","material","node","physics","render","terrain","texture","UI",
"workspace","vector","algorithm","array","boolean","buffer","class","compiler","coroutine","debug",
"enum","iterator","method","namespace","parameter","recursive","stack","variable"]

GREATNAME = ["roblox","hex","mod","telamon","builderman","tix","diamond","epic"]

JOBLIST = ["artist","engineer","worker","painter","programmer","coder","teacher","musician","lawyer"]

# File paths
LOG_FOLDER = "DuckSnipeLogs"
USERS_FILE = "users.txt"
WORDS_FILE = "words.txt"
AVAILABLE_FILE = "available_usernames.txt"  # New file for available usernames

# Global state
AVAILABLE_SNIPES = []
CUSTOM_WORDS = []