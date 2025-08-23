import requests
import random
from colorama import Fore, Style
import os
import time

os.system('cls')

availableSnipes = []
error = False

version = "1.0.41"

lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']
dbl = ['aa', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo', 'pp', 'qq', 'rr', 'ss',
       'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz']
special = ['*','@','%','!','.','&','#']
num = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
all = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
       'w', 'x', 'y', 'z', "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "_"]
allVariant = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z', "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
wordlist = ["verified", "public", "sound", "un", "war", "star", "course", "glitch", "glitched", "private", "secure",
            "taste", "test", "tested", "taken", "build", "bought", "built", "tower", "script", "scripted", "house",
            "sky", "building", "bank", "special", "demo", "gun", "money", "obvious", "vampire", "wicked", "lua", "code",
            "object", "dirt", "stone", "rock", "sand", "water", "lava", "fire", "brick", "badge", "guest", "copper",
            "tree", "tire", "orange", "mouse", "paper", "wire", "cord", "light", "thunder", "rain", "word", "blood",
            "duck", "ducky", "snipe", "rifle", "god", "angel", "ground", "grass", "internet", "social", "socially",
            "google", "guilded", "web", "hunt", "cute", "skull", "legal", "legally", "mc", "legal", "wild", "crazy",
            "dox", "bin", "ban", "banned", "banish", "banished", "og", "roblox", "swat", "epic", "epik", "sent", "tix",
            "module", "local", "bot", "bucket", "secret", "weapon", "storage", "wish", "wind", "whole", "plays", "forest", "sub", "leave", "pole", "pong", "like", "live", "quant", "count", "let", "fork", "reduce", "bacon", "limited", "unlimited", "fix", "fixed", "broken", "shattered"]
minerals = ["dirt", "stone", "rock", "sand", "water", "lava", "fire", "copper", "rain", "ruby", "diamond", "sapphire",
            "gem", "mud", "earth", "air", "amethyst"]
rbxstudio = ["model", "mesh", "part", "audio", "tool", "decal", "animation", "collider", "constraint", "controller", "emitter", "keyframe", "material", "node", "physics", "render", "terrain", "texture", "UI", "workspace", "vector", "algorithm", "array", "boolean", "buffer", "class", "compiler", "coroutine", "debug", "enum", "iterator", "method", "namespace", "parameter", "recursive", "stack", "variable"]
greatname = ["roblox", "hex", "mod", "telamon", "builderman", "tix", "diamond", "epic"]
joblist = ["artists", "engineer", "worker", "painter", "job", "programmer", "coder", "teacher", "musician", "lawyer", "officer", "legislator"]
colors = [Fore.RED, Fore.GREEN, Fore.CYAN, Fore.YELLOW]
custom = [""]

def syncWords():
    global custom
    try:
        f = open("words.txt", "r")
        customwords = f.read()
        x = customwords.split(",")
        x.remove('')
        custom = x
    except:
        pass

def validate_username(username):
    url = f"https://auth.roblox.com/v1/usernames/validate?birthday=2006-09-21T07:00:00.000Z&context=Signup&username={username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0:
            print(f"{Fore.GREEN}" + username + f" is available for use.{Style.RESET_ALL}")
            availableSnipes.append(username)
        elif data['code'] == 1:
            print(f"{Fore.RED}" + username + f" is taken.{Style.RESET_ALL}")
        elif data['code'] == 2:
            print(f"{Fore.RED}" + username + f" is not appropriate for roblox.{Style.RESET_ALL}")
        elif data['code'] == 10:
            print(username + " may contain private information.")
    else:
        print("Unable to access Roblox API")


# on start

def onstart():
    global error
    error = False
    syncWords()
    randomColor = random.choice(colors)
    print(" ")
    print(f"{randomColor} [ DuckSnipe - {version} ]{Style.RESET_ALL}")
    print(" ")
    print(" do cmds for all roblox name snipe commands.")
    print(" ")
    cmd = input(f"{randomColor}==> {Style.RESET_ALL}")
    print(" ")

    splitcmd = cmd.split(" ")

    # commands
    if cmd == "cmds":
        print("[ Commands ]")
        print(" ")
        print("gens [gen/key] - Get all working generators.")
        print("gen [type] [att] - Generate Untaken Names.")
        print("genkey [type] [key] - Generate Untaken Names with a keyword.")
        print("check [name] - Check Name for availability.")
        print("pass [name] - Generates & saves a password for an account.")
        print("addacc [username] [password] - Saves account to snipe storage.")
        print("storage - Shows all your saved users.")
        print("")
        print("[ Terms ]")
        print(" ")
        print("# - replaced with a number")
        print("* - replaced with a letter")
        print("")
        input("Press Enter to go back. ")
        os.system('cls')
        onstart()
    if splitcmd[0] == "gens":
        try:
            if splitcmd[1] == "gen":
                print("[ Regular Gen ]")
                print(" ")
                print("4l [attempts] - Generates 4 letters.")
                print("4char [attempts] - Generates 4 chars.")
                print("5l [attempts] - Generates 5 letters.")
                print("5char [attempts] - Generates 5 chars.")
                print("6l [attempts] - Generates 6 letters.")
                print("6char [attempts] - Generates 6 chars.")
                print("")
                input("Press Enter to go back. ")
                os.system('cls')
                onstart()
            if splitcmd[1] == "key":
                print("[ GenKey ]")
                print(" ")
                print("##key [key] - Generates 2 digits BEFORE the key 10-100")
                print("key## [key] - Generates 2 digits AFTER the key 10-100")
                print("#key [key] - Generates 1 num BEFORE the key 0-9")
                print("key# [key] - Generates 1 num AFTER the key 0-9")
                print("wordlist [key] - Generates names with wordlist and your key.")
                print("wordlist_ [key] - Generates names with wordlist and your key but with an _")
                print("studio [key] - Generates names with roblox studio terms and your key.")
                print("studio_ [key] - Generates names with roblox studio terms and your key but with an _")
                print("jobs [key] - Generates names with jobs and your key.")
                print("jobs_ [key] - Generates names with jobs and your key but with an _")
                print("minerals [key] - Generates names with minerals and your key.")
                print("custom [key] - Generates names with your custom wordlist and your key.")
                print("great [key] - Generates names with well-known keywords and your key.")
                print("key** - Generates 2 letters after the key. (ex: keyAA)")
                print("key* - Generates a letter after the key. (ex: keyA)")
                print("*_key - Generates a letter before the key but with an _ (ex: A_key)")
                print("#_key - Generates 1 num before the key 0-9 but with an _ (ex: 0_key)")
                print("")
                input("Press Enter to go back. ")
                os.system('cls')
                onstart()
        except IndexError:
            error = True
            print(f"{Fore.RED} Something went wrong. Did you forget to add an argument?{Style.RESET_ALL}")
            time.sleep(3)
            os.system('cls')
            onstart()

    if splitcmd[0] == "genkey":
        try:
            if splitcmd[1] == "wordlist":
                for i in wordlist:
                    validate_username(splitcmd[2] + i)
                for i in wordlist:
                    validate_username(i + splitcmd[2])
            if splitcmd[1] == "wordlist_":
                for i in wordlist:
                    validate_username(splitcmd[2] + "_" + i)
                for i in wordlist:
                    validate_username(i + "_" + splitcmd[2])
            if splitcmd[1] == "studio":
                for i in rbxstudio:
                    validate_username(splitcmd[2] + i)
                for i in rbxstudio:
                    validate_username(i + splitcmd[2])
            if splitcmd[1] == "studio_":
                for i in rbxstudio:
                    validate_username(splitcmd[2] + "_" + i)
                for i in rbxstudio:
                    validate_username(i + "_" + splitcmd[2])
            if splitcmd[1] == "minerals":
                for i in minerals:
                    validate_username(splitcmd[2] + i)
                for i in minerals:
                    validate_username(i + splitcmd[2])
            if splitcmd[1] == "custom":
                for i in custom:
                    validate_username(splitcmd[2] + i)
                for i in custom:
                    validate_username(i + splitcmd[2])
            if splitcmd[1] == "great":
                for i in greatname:
                    validate_username(splitcmd[2] + i)
                for i in greatname:
                    validate_username(i + splitcmd[2])
            if splitcmd[1] == "jobs":
                for i in joblist:
                    validate_username(splitcmd[2] + i)
                for i in joblist:
                    validate_username(i + splitcmd[2])
            if splitcmd[1] == "jobs_":
                for i in joblist:
                    validate_username(splitcmd[2] + "_" + i)
                for i in joblist:
                    validate_username(i + "_" + splitcmd[2])
            if splitcmd[1] == "##key":
                for a in range(10, 100):
                    validate_username(str(a) + splitcmd[2])
            if splitcmd[1] == "key##":
                for a in range(10, 100):
                    validate_username(splitcmd[2] + str(a))
            if splitcmd[1] == "#key":
                for a in range(0, 10):
                    validate_username(str(a) + splitcmd[2])
            if splitcmd[2] == "key#":
                for a in range(0, 10):
                    validate_username(splitcmd[2] + str(a))
            if splitcmd[1] == "#_key":
                for a in range(0, 10):
                    validate_username(str(a) + "_" + splitcmd[2])
                for a in range(0, 10):
                    validate_username(splitcmd[2] + "_" + str(a))
            if splitcmd[1] == "*_key":
                for a in lower:
                    validate_username(str(a) + "_" + splitcmd[2])
                for a in lower:
                    validate_username(splitcmd[2] + "_" + str(a))
            if splitcmd[1] == "key*":
                for i in lower:
                    validate_username(splitcmd[2] + i)
                for i in lower:
                    validate_username(i + splitcmd[2])
            if splitcmd[1] == "key**":
                for i in dbl:
                    validate_username(splitcmd[2] + i)
                for i in dbl:
                    validate_username(i + splitcmd[2])
        except IndexError:
            error = True
            print(f"{Fore.RED} Something went wrong. Did you forget to add an argument?{Style.RESET_ALL}")
            time.sleep(3)
            os.system('cls')
            onstart()

    if cmd == "storage":
        try:
            print("")
            print(f"{Fore.CYAN}[ Your saved users ]{Style.RESET_ALL}")
            print("")
            f = open("users.txt", "r")
            print(f.read())
        except FileNotFoundError:
            print("")
            print(f"{Fore.RED}No saved users found.{Style.RESET_ALL}")
        print("")
        input("Press Enter to go back.")
        os.system('cls')
        onstart()

    if splitcmd[0] == "addword":
        try:
            with open('words.txt', 'a') as file:
                file.write(splitcmd[1] + ",")
            print("")
            print(f"{Fore.CYAN}[ Saved word: {splitcmd[1]} to wordlist! ]{Style.RESET_ALL}")
            print("")
            time.sleep(3)
            os.system('cls')
            onstart()
        except IndexError:
            error = True
            print(f"{Fore.RED} Something went wrong. Did you forget to add an argument?{Style.RESET_ALL}")
            time.sleep(3)
            os.system('cls')
            onstart()

    if splitcmd[0] == "gen":
        try:
            if splitcmd[1] == "4l":
                for a in range(int(splitcmd[2])):
                    validate_username(
                        random.choice(lower) + random.choice(lower) + random.choice(lower) + random.choice(lower))
            if splitcmd[1] == "4char":
                for a in range(int(splitcmd[2])):
                    validate_username(
                        random.choice(allVariant) + random.choice(all) + random.choice(all) + random.choice(allVariant))
            if splitcmd[1] == "5char":
                for a in range(int(splitcmd[2])):
                    validate_username(random.choice(allVariant) + random.choice(all) + random.choice(all) + random.choice(
                        all) + random.choice(allVariant))
            if splitcmd[1] == "5l":
                for a in range(int(splitcmd[2])):
                    validate_username(random.choice(lower) + random.choice(lower) + random.choice(lower) + random.choice(
                        lower) + random.choice(lower))
            if splitcmd[1] == "6l":
                for a in range(int(splitcmd[2])):
                    validate_username(random.choice(lower) + random.choice(lower) + random.choice(lower) + random.choice(
                        lower) + random.choice(lower) + random.choice(lower))
            if splitcmd[1] == "6char":
                for a in range(int(splitcmd[2])):
                    validate_username(random.choice(allVariant) + random.choice(all) + random.choice(all) + random.choice(
                        all) + random.choice(all) + random.choice(allVariant))
        except IndexError:
            error = True
            print(f"{Fore.RED} Something went wrong. Did you forget to add an argument?{Style.RESET_ALL}")
            time.sleep(3)
            os.system('cls')
            onstart()

    if splitcmd[0] == "check":
        try:
            validate_username(splitcmd[1])
            time.sleep(3)
            os.system('cls')
            onstart()
        except IndexError:
            print(f"{Fore.RED} Enter a valid username.{Style.RESET_ALL}")
            time.sleep(3)
            os.system('cls')
            onstart()
    if splitcmd[0] == "pass":
        try:
            generatedpass = ""
            chance = random.randint(1, 2)
            if chance == 1:
                thing = splitcmd[1] + "-"
                randomword = random.choice(wordlist) + "-"
                randomnum = str(random.randint(100, 1000))
                randomspecial = random.choice(special)
                generatedpass = thing + randomword + randomnum + randomspecial
            else:
                thing = splitcmd[1] + "-"
                randomword = random.choice(wordlist) + "-"
                randomnum = str(random.randint(100, 1000))
                randomspecial = random.choice(special)
                generatedpass = randomword + thing + randomnum + randomspecial
            with open('users.txt', 'a') as file:
                file.write(splitcmd[1] + " : " + generatedpass + "\n")
            print(" ")
            print(f"{Fore.YELLOW}Generated Password:{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{generatedpass}{Style.RESET_ALL}")
            print("")
            print(f"{Fore.CYAN}[ Saved Username & Password to file! ]{Style.RESET_ALL}")
            print("")
            input("Press Enter to go back.")
            os.system('cls')
            onstart()
        except IndexError:
            print(f"{Fore.RED} Enter a valid username.{Style.RESET_ALL}")
            time.sleep(3)
            os.system('cls')
            onstart()

    if splitcmd[0] == "addacc":
        try:
            with open('users.txt', 'a') as file:
                file.write(splitcmd[1] + " : " + splitcmd[2] + "\n")
            print(" ")
            print(f"{Fore.GREEN}[ Added account '{splitcmd[1]}' to snipe storage! ]{Style.RESET_ALL}")
            print("")
            print(f"{Fore.YELLOW}-=- Info -=-{Style.RESET_ALL}")
            print(f"Username: {splitcmd[1]}")
            print(f"Password: {splitcmd[2]}")
            print("")
            input("Press Enter to go back.")
            os.system('cls')
            onstart()
        except IndexError:
            print(f"{Fore.RED} Something went wrong. Did you forget an argument?{Style.RESET_ALL}")
            time.sleep(3)
            os.system('cls')
            onstart()

    nocommand = ["check", "cmds", "pass"]
    yescommand = ["gen", "gens", "genkey"]
    if not splitcmd[0] in nocommand:
        if availableSnipes:
            print(" ")
            print(f"{Fore.BLUE} [ Store available users in file? ]{Style.RESET_ALL}")
            choice = input("(y/n): ")
            if choice == "y":
                with open('valid.txt', 'a') as file:
                    for a in availableSnipes:
                        file.write(a + '\n')
                    file.write("\n")
            availableSnipes.clear()
            os.system('cls')
            onstart()
        else:
            if not error:
                if splitcmd[0] in yescommand:
                    print(" ")
                    print(f"All generated users are {Fore.RED}taken{Style.RESET_ALL} :[")
                    time.sleep(2.5)
                    availableSnipes.clear()
                    os.system('cls')
                    onstart()
                else:
                    print(" ")
                    print(f"{Fore.RED}Unknown command:{Style.RESET_ALL} {splitcmd[0]}")
                    time.sleep(1)
                    availableSnipes.clear()
                    os.system('cls')
                    onstart()

if __name__ == "__main__":
    onstart()
