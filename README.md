# DuckSnipe

**Open-source Roblox username availability checker with advanced features**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.9-orange.svg)](https://github.com/daredjumper/ducksnipe)

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Commands](#commands) • [Settings](#settings)

---

## Features

- **Concurrent Checking** - Fast async username validation with configurable rate limiting
- **Smart Generation** - Multiple wordlist types for username combinations (270+ words)
- **Random Generator** - Create random letter-based usernames with customizable length
- **Password Generator** - Automatic secure password creation
- **Storage System** - Save accounts and track available usernames automatically
- **Detailed Logging** - Comprehensive logs with timestamps in dedicated folder
- **Custom Wordlists** - Add your own words for personalized generation
- **Color-Coded Output** - Beautiful terminal interface with colored status messages
- **Settings Management** - Interactive configuration for API and file paths
- **Rate Limit Detection** - Automatic detection and warnings for API throttling
- **Persistent Settings** - Save configurations between sessions

---

## Installation

### Quick Setup (Recommended)

1. Clone the repository
   ```bash
   git clone https://github.com/daredjumper/ducksnipe.git
   cd ducksnipe
   ```

2. Run the auto-installer
   ```bash
   install.bat
   ```

3. Launch DuckSnipe
   ```bash
   start.bat
   ```

### Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install aiohttp colorama

# Run application
python ducksnipe.py
```

---

## Usage

### Quick Start

```bash
# Generate and check usernames from wordlist
genkey wordlist Pro

# Generate random 5-character usernames
letter_gen

# Check specific usernames
check CoolDude123 EpicGamer456

# View all available usernames found
available

# Modify settings (rate limiting, file paths)
settings
```

### Example Workflow

```bash
# Step 1: Generate usernames
genkey wordlist Shadow
# Generates: Shadowpro, proShadow, Shadowking, kingShadow, etc.

# Step 2: View available usernames
available
# Shows all usernames that are available

# Step 3: Generate password for available username
pass ShadowKing

# Step 4: Save account
addacc ShadowKing MySecurePass123
```

---

## Commands

### Username Generation

| Command | Description | Example |
|---------|-------------|---------|
| `genkey [type] [key]` | Generate username combinations from wordlist | `genkey wordlist Pro` |
| `letter_gen` | Interactive random username generator | `letter_gen` |
| `check [username...]` | Check specific username availability | `check User1 User2` |

### Data Management

| Command | Description | Example |
|---------|-------------|---------|
| `available` | View all available usernames found | `available` |
| `storage` | View saved accounts | `storage` |
| `addword [word]` | Add custom word to wordlist | `addword shadow` |
| `pass [username]` | Generate random password | `pass MyUsername` |
| `addacc [user] [pass]` | Save account credentials | `addacc User Pass123` |

### Configuration

| Command | Description | Example |
|---------|-------------|---------|
| `settings` | View and modify settings | `settings` |
| `clear` | Clear available snipes from memory | `clear` |
| `help` | Show detailed help guide | `help` |
| `cmds` | Show command list | `cmds` |

### Wordlist Types

- **wordlist** - 270+ common words and gaming terms
- **studio** - Roblox Studio terminology and API references
- **minerals** - Mineral, element, and gem names
- **custom** - Your personal custom wordlist
- **great** - Premium Roblox-related words
- **jobs** - Professions and occupations

---

## Settings

Access the settings menu with the `settings` command to configure:

### API Settings
- **Max Concurrent Requests** (Default: 10)
  - Number of simultaneous API requests
  - Lower values = safer, less likely to be rate limited
  - Range: 1-100

- **Request Delay** (Default: 0.3 seconds)
  - Delay between request batches
  - Higher values = safer, slower checking
  - Range: 0-10 seconds

### File Paths
- **Log Folder** - Where logs are saved (Default: DuckSnipeLogs)
- **Users File** - Account storage location (Default: users.txt)
- **Words File** - Custom wordlist location (Default: words.txt)
- **Available File** - Available usernames log (Default: available_usernames.txt)

### Reset to Defaults
Option to reset all settings to safe default values.

---

## File Structure

```
ducksnipe/
├── ducksnipe.py          # Main application entry point
├── config.py             # Configuration and wordlists
├── api.py                # Async API handling
├── commands.py           # Command implementations
├── utils.py              # Utility functions
├── install.bat           # Windows auto-installer
├── start.bat             # Quick launcher
├── settings.json         # Saved settings (auto-created)
├── words.txt             # Custom wordlist (auto-created)
├── users.txt             # Saved accounts (auto-created)
├── available_usernames.txt  # Available usernames log (auto-created)
└── DuckSnipeLogs/        # Execution logs (auto-created)
    ├── genkey_output.txt
    ├── check_output.txt
    ├── letter_gen_output.txt
    ├── rate_limit_output.txt
    ├── rate_limit_alerts.txt
    ├── timeouts_output.txt
    ├── connection_errors_output.txt
    └── errors_output.txt
```

---

## How It Works

### Username Generation
1. Combines your key with wordlist entries (e.g., "Pro" + "Shadow" = "ProShadow", "ShadowPro")
2. Or generates random letter-based usernames with configurable length and number inclusion

### Availability Checking
1. Uses Roblox auth API to validate username availability
2. Checks multiple usernames concurrently with rate limiting
3. Color-coded output shows status: available (green), taken (red), inappropriate (yellow)

### Data Storage
1. Available usernames automatically saved to `available_usernames.txt` with timestamps
2. Account credentials saved to `users.txt`
3. All operations logged to `DuckSnipeLogs/` folder

### Rate Limit Protection
1. Configurable concurrent request limits
2. Adjustable delays between requests
3. Automatic detection of 429/403 status codes
4. Warning messages with recommendations

---

## Rate Limiting

DuckSnipe includes smart rate limiting to prevent API bans:

### Default Safe Settings
- 10 concurrent requests
- 0.3 second delay between batches
- Automatic rate limit detection

### If Rate Limited
1. Wait 5-10 minutes before retrying
2. Use `settings` to lower Max Concurrent Requests (try 5)
3. Use `settings` to increase Request Delay (try 0.5 or 1.0)
4. Check logs in `DuckSnipeLogs/rate_limit_alerts.txt`

### Best Practices
- Start with default settings
- Only increase speed if no rate limiting occurs
- Monitor `rate_limit_output.txt` for warnings
- Use lower settings for mass checking (1000+ usernames)

---

## Advanced Features

### Letter Generator
Interactive random username generator with:
- Custom length (3-20 characters)
- Count selection (1-50000 or 'max' for maximum possible)
- Optional number inclusion
- Duplicate prevention
- Automatic availability checking

Example:
```
letter_gen
> Characters: 5
> Count: max
> Include numbers? (y/n): y
> Generating 50000 usernames...
```

### Color-Coded Interface
- Green: Available usernames and success messages
- Red: Taken usernames, errors, rate limits
- Yellow: Warnings and inappropriate usernames
- Cyan: Information and status messages
- Magenta: Command prompts and headers

### Persistent Settings
Settings are saved to `settings.json` and automatically loaded on startup. No need to reconfigure each time.

---

## Troubleshooting

### Rate Limiting (429/403 Errors)
**Solution:** Lower concurrent requests and add delay in settings menu

### "Module has no attribute" Errors
**Solution:** Ensure all files (config.py, api.py, commands.py, utils.py, ducksnipe.py) are updated to latest version

### Import Errors
**Solution:** Run `pip install aiohttp colorama` or use `install.bat`

### Logs Not Saving
**Solution:** Check write permissions for DuckSnipeLogs folder

---

## Disclaimer

This tool is for **educational purposes only**. 

- Username sniping may violate Roblox Terms of Service
- Use responsibly and ethically
- Respect rate limits to avoid IP bans
- The developers are not responsible for any misuse
- Use at your own risk

---

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

## Credits

Made by the community for the community

[Report Bug](https://github.com/daredjumper/ducksnipe/issues) • [Request Feature](https://github.com/daredjumper/ducksnipe/issues) • [Discussions](https://github.com/daredjumper/ducksnipe/discussions)
