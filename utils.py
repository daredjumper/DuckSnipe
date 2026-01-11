"""
DuckSnipe Utilities
Helper functions for file operations and logging
"""

import os
import re
import json
from datetime import datetime
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Import config values
import config

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def sync_custom_words():
    """Load custom words from file"""
    try:
        with open(config.WORDS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            config.CUSTOM_WORDS[:] = [w.strip() for w in content.split(",") if w.strip()]
    except FileNotFoundError:
        config.CUSTOM_WORDS.clear()
        with open(config.WORDS_FILE, "w", encoding="utf-8") as f:
            pass

def load_settings():
    """Load settings from JSON file"""
    try:
        with open(config.SETTINGS_FILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
            
            # Update config with saved settings
            config.LOG_FOLDER = settings.get("log_folder", config.LOG_FOLDER)
            config.USERS_FILE = settings.get("users_file", config.USERS_FILE)
            config.WORDS_FILE = settings.get("words_file", config.WORDS_FILE)
            config.AVAILABLE_FILE = settings.get("available_file", config.AVAILABLE_FILE)
            config.MAX_CONCURRENT_REQUESTS = settings.get("max_concurrent_requests", config.MAX_CONCURRENT_REQUESTS)
            config.REQUEST_DELAY = settings.get("request_delay", config.REQUEST_DELAY)
            
            return True
    except FileNotFoundError:
        save_settings()  # Create default settings file
        return False
    except Exception as e:
        print(f"{Fore.RED}Error loading settings: {e}")
        return False

def save_settings():
    """Save current settings to JSON file"""
    settings = {
        "log_folder": config.LOG_FOLDER,
        "users_file": config.USERS_FILE,
        "words_file": config.WORDS_FILE,
        "available_file": config.AVAILABLE_FILE,
        "max_concurrent_requests": config.MAX_CONCURRENT_REQUESTS,
        "request_delay": config.REQUEST_DELAY
    }
    
    try:
        with open(config.SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error saving settings: {e}")
        return False

def log_message(command_name, text):
    """Strip ANSI color codes and append to log file in DuckSnipeLogs folder"""
    plain = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = os.path.join(config.LOG_FOLDER, f"{command_name}_output.txt")
    
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {plain}\n")
    except Exception as e:
        print(f"{Fore.YELLOW}Warning: Could not write to log: {e}")

def save_rate_limit_alert(error_type, username):
    """Save rate limit alerts to dedicated log file in DuckSnipeLogs folder"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = os.path.join(config.LOG_FOLDER, "rate_limit_alerts.txt")
    
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {error_type} - Username: {username}\n")
            f.write(f"[{timestamp}] RECOMMENDATION: Lower MAX_CONCURRENT_REQUESTS or increase REQUEST_DELAY\n")
            f.write("-" * 80 + "\n")
    except Exception as e:
        print(f"{Fore.YELLOW}Warning: Could not write rate limit alert: {e}")

def safe_file_write(filepath, content, mode="a"):
    """Safely write to file with error handling"""
    try:
        with open(filepath, mode, encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error writing to {filepath}: {e}")
        log_message("file_errors", f"Failed to write to {filepath}: {e}")
        return False

def safe_file_read(filepath):
    """Safely read from file with error handling"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"{Fore.RED}Error reading {filepath}: {e}")
        log_message("file_errors", f"Failed to read from {filepath}: {e}")
        return None