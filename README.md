<div align="center">

# DuckSnipe

**Open-source Roblox username availability checker**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.8-orange.svg)](https://github.com/yourusername/ducksnipe)

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Commands](#commands)

</div>

---

## Features

- **Concurrent Checking** - Fast async username validation
- **Smart Generation** - Multiple wordlist types for username combinations
- **Password Generator** - Automatic secure password creation
- **Storage System** - Save accounts and available usernames
- **Detailed Logging** - Track all checks with timestamps and execution times
- **Custom Wordlists** - Add your own words for personalized generation

---

## Installation

### Quick Setup

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/ducksnipe.git
   cd ducksnipe
   ```

2. Run the installer
   ```bash
   install.bat
   ```

3. Launch DuckSnipe
   ```bash
   start.bat
   ```

### Manual Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install aiohttp
python ducksnipe.py
```

---

## Usage

### Basic Commands

```bash
# Generate and check usernames
genkey wordlist Pro

# Check specific usernames
check CoolDude123 EpicGamer456

# Add custom words
addword ninja

# Generate password
pass CoolDude123

# View saved accounts
storage
```

---

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `genkey [type] [key]` | Generate username combinations | `genkey wordlist Pro` |
| `check [username]` | Check username availability | `check TestUser123` |
| `addword [word]` | Add custom word to wordlist | `addword shadow` |
| `pass [username]` | Generate random password | `pass MyUsername` |
| `addacc [user] [pass]` | Save account credentials | `addacc User Pass123` |
| `storage` | View saved accounts | `storage` |
| `clear` | Clear available snipes list | `clear` |
| `help` | Show detailed help | `help` |

### Wordlist Types

- **wordlist** - Common words and terms
- **studio** - Roblox Studio terminology
- **minerals** - Mineral and element names
- **custom** - Your personal wordlist
- **great** - Premium Roblox-related words
- **jobs** - Professions and occupations

---

## File Structure

```
ducksnipe/
├── ducksnipe.py        # Main application
├── install.bat         # Auto-installer
├── start.bat           # Quick launcher
├── words.txt           # Custom wordlist (auto-created)
├── users.txt           # Saved accounts (auto-created)
└── DuckSnipeLogs/      # Execution logs (auto-created)
    ├── genkey_output.txt
    ├── check_output.txt
    └── ...
```

---

## How It Works

1. Generate usernames by combining your key with wordlist entries
2. Check availability using Roblox's validation API concurrently
3. Store available usernames and generated passwords
4. Log all operations with timestamps and execution metrics

---

## Disclaimer

This tool is for **educational purposes only**. Username sniping may violate Roblox Terms of Service. Use responsibly and at your own risk.

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

<div align="center">

**Made by the community**

[Report Bug](https://github.com/yourusername/ducksnipe/issues) • [Request Feature](https://github.com/yourusername/ducksnipe/issues)

</div>