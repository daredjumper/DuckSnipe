"""
DuckSnipe - Main Entry Point
Roblox username availability checker
"""

import os
import asyncio
from config import VERSION, LOG_FOLDER
from utils import sync_custom_words, log_message
from commands import (add_word, generate_pass, add_account, show_storage,
                      show_commands, show_help, clear_snipes, 
                      handle_genkey, handle_check)

def initialize():
    """Initialize application"""
    os.makedirs(LOG_FOLDER, exist_ok=True)
    sync_custom_words()

def main():
    """Main application loop"""
    initialize()
    
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
            
            # Exit commands
            if cmd in ["exit", "quit"]:
                print("Thanks for using DuckSnipe! Goodbye.")
                break
            
            # Synchronous commands
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
            
            # Asynchronous commands
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