"""
DuckSnipe - Main Entry Point
Roblox username availability checker
"""

import os
import asyncio
from colorama import Fore, Back, Style, init
import config
from utils import sync_custom_words, log_message, load_settings
from commands import (add_word, generate_pass, add_account, show_storage,
                      show_commands, show_help, clear_snipes, show_available,
                      handle_genkey, handle_check, handle_letter_gen,
                      show_settings, modify_settings)

# Initialize colorama
init(autoreset=True)

def initialize():
    """Initialize application"""
    os.makedirs(config.LOG_FOLDER, exist_ok=True)
    load_settings()  # Load settings from file
    sync_custom_words()

def main():
    """Main application loop"""
    initialize()
    
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════╗
║{Fore.YELLOW}     DuckSnipe v{config.VERSION} Started      {Fore.CYAN}║
╚═══════════════════════════════════════╝{Style.RESET_ALL}

{Fore.GREEN}Type 'help' for guide or 'cmds' for command list{Style.RESET_ALL}
""")
    
    while True:
        try:
            cmd_input = input(f"\n{Fore.MAGENTA}==>{Style.RESET_ALL} ").strip()
            
            if not cmd_input:
                continue
            
            parts = cmd_input.split()
            cmd = parts[0].lower()
            args = parts[1:]
            
            # Exit commands
            if cmd in ["exit", "quit"]:
                print(f"{Fore.YELLOW}Thanks for using DuckSnipe! Goodbye.{Style.RESET_ALL}")
                break
            
            # Synchronous commands
            elif cmd == "cmds":
                show_commands()
                
            elif cmd == "help":
                show_help()
                
            elif cmd == "settings":
                show_settings()
                modify_settings()
                
            elif cmd == "available":
                show_available()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
            elif cmd == "addword":
                if args:
                    add_word(args[0])
                else:
                    print(f"{Fore.YELLOW}Usage: addword [word]")
                    
            elif cmd == "pass":
                if args:
                    generate_pass(args[0])
                else:
                    print(f"{Fore.YELLOW}Usage: pass [username]")
                    
            elif cmd == "addacc":
                if len(args) >= 2:
                    add_account(args[0], args[1])
                else:
                    print(f"{Fore.YELLOW}Usage: addacc [username] [password]")
                    
            elif cmd == "storage":
                show_storage()
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
            elif cmd == "clear":
                clear_snipes()
            
            # Asynchronous commands
            elif cmd == "genkey":
                asyncio.run(handle_genkey(args))
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
            elif cmd == "letter_gen":
                asyncio.run(handle_letter_gen())
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
            elif cmd == "check":
                asyncio.run(handle_check(args))
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
                
            else:
                print(f"{Fore.RED}Unknown command: '{cmd}'")
                print(f"{Fore.YELLOW}Type 'help' for assistance or 'cmds' for command list")
        
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Interrupted. Type 'exit' to quit.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
            log_message("error", f"Unexpected error: {e}")

if __name__ == "__main__":
    main()