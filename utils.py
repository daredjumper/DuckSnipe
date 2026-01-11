"""
DuckSnipe Utilities
Helper functions for file operations and logging
"""

import os
import re
from datetime import datetime
from config import LOG_FOLDER, WORDS_FILE, CUSTOM_WORDS

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def sync_custom_words():
    """Load custom words from file"""
    global CUSTOM_WORDS
    try:
        with open(WORDS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            CUSTOM_WORDS[:] = [w.strip() for w in content.split(",") if w.strip()]
    except FileNotFoundError:
        CUSTOM_WORDS.clear()
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