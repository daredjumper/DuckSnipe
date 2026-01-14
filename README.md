# DuckSnipe

Open-source Roblox username availability checker with CLI & Web Interface

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.9-orange.svg)](https://github.com/daredjumper/ducksnipe)

---

## Overview

DuckSnipe is a powerful tool for checking Roblox username availability. It offers both a command-line interface for power users and a modern web interface for visual interaction. Built with async operations and smart rate limiting to ensure fast, reliable results while respecting API limits.

**Key Capabilities:**
- Concurrent username checking with configurable rate limiting
- Multiple generation methods: wordlist combinations, random letters, number patterns
- Dual interface: CLI for speed, Web for visualization
- Comprehensive logging and result tracking
- Real-time statistics dashboard
- JSON export functionality

---

## Quick Start

### Installation

**Automated Setup (Windows)**
```bash
git clone https://github.com/daredjumper/ducksnipe.git
cd ducksnipe
install.bat
```

The installer will automatically:
- Create virtual environment
- Install all dependencies (aiohttp, colorama, Flask)
- Set up required folders and files

**Manual Setup**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install aiohttp colorama flask
```

### Running

**Interactive Launcher**
```bash
start.bat
```

Select your preferred mode:
- [1] CLI Mode - Traditional command-line interface
- [2] Web Interface - Browser-based GUI at localhost:8080
- [3] Dual Mode - Run both simultaneously

**Direct Launch**
```bash
python ducksnipe.py  # CLI
python web_server.py  # Web interface
```

---

## Features

### Core Functionality

**Username Generation**
- GenKey: Combine custom keys with predefined wordlists (270+ words)
- Letter Generator: Random letter-based usernames with customizable parameters
- Number Generator: Pure numbers, prefix/suffix combinations, or sequential ranges

**Checking & Validation**
- Async concurrent checking for maximum speed
- Configurable rate limiting to prevent API bans
- Automatic detection of rate limit responses (429/403)
- Color-coded status output for quick scanning

**Data Management**
- Automatic saving of available usernames with timestamps
- Account credential storage
- Custom wordlist support
- Comprehensive logging system
- JSON export capability

### Interface Options

**Command-Line Interface**
- Fast command execution
- Full feature access via text commands
- Ideal for automation and power users
- Persistent settings across sessions

**Web Interface**
- Modern, responsive design
- Live statistics dashboard
- Interactive generators with real-time feedback
- Visual result display
- One-click JSON export
- Auto-refreshing stats every 5 seconds

---

## Usage

### CLI Commands

**Generation**
```bash
genkey [type] [key]    # Generate combinations from wordlist
letter_gen             # Interactive random letter generator
genum                  # Interactive number generator
check [username...]    # Check specific usernames
```

**Data Management**
```bash
available              # View available usernames
storage                # View saved accounts
addword [word]         # Add to custom wordlist
pass [username]        # Generate password
addacc [user] [pass]   # Save account credentials
clear                  # Clear in-memory results
```

**Configuration**
```bash
settings               # View/modify settings
web                    # Launch web interface
help                   # Detailed help
cmds                   # Command list
```

### Web Interface

Navigate to `http://localhost:8080` after starting the web server.

**Quick Check Tab**
Enter usernames line-by-line to check availability instantly.

**Generator Tabs**
- **GenKey**: Select wordlist type and key value
- **Letters**: Configure length, count, and number inclusion
- **Numbers**: Choose from pure numbers, prefix/suffix combos, or sequential ranges

**Results Panel**
View all available usernames with timestamps, refresh manually, or export to JSON.

### Example Workflow

```bash
# Start dual mode
start.bat → [3]

# Generate via CLI
=> genkey wordlist Shadow

# Monitor via Web
# Results appear in real-time on dashboard

# Export findings
# Click "Export JSON" in web interface

# Save credentials
=> pass ShadowKing
=> addacc ShadowKing GeneratedPassword123
```

---

## Configuration

### API Settings

Access via CLI `settings` command or Web interface.

**Max Concurrent Requests** (Default: 10)
- Simultaneous API requests
- Lower = safer, higher = faster
- Range: 1-100
- Recommended: 5-10 for safe operation

**Request Delay** (Default: 0.3s)
- Pause between request batches
- Higher = safer, lower = faster
- Range: 0-10 seconds
- Recommended: 0.3-0.5 for safe operation

### File Paths

All paths are configurable:
- Log Folder: `DuckSnipeLogs`
- Users File: `users.txt`
- Words File: `words.txt`
- Available File: `available_usernames.txt`

Settings persist to `settings.json` automatically.

---

## Wordlist Types

**wordlist** - 270+ common words and gaming terms  
**studio** - Roblox Studio terminology and API references  
**minerals** - Mineral, element, and gem names  
**custom** - Your personal wordlist (add via `addword`)  
**great** - Premium Roblox-related words  
**jobs** - Professions and occupations

---

## Number Generator

Four generation modes:

**Pure Numbers**
Generate random numbers with specified digit length (1-10).
Example: 12345, 98765

**Prefix + Numbers**
Add text before numbers, validates total length.
Example: User12345, Pro98765

**Numbers + Suffix**
Add text after numbers, validates total length.
Example: 12345Pro, 98765Epic

**Sequential Range**
Generate consecutive numbers within range.
Example: 10000-11000

---

## Web API

RESTful API available at `http://localhost:8080/api`:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stats` | GET | Current statistics |
| `/api/available` | GET | Available usernames list |
| `/api/check` | POST | Check usernames |
| `/api/genkey` | POST | Generate with wordlists |
| `/api/letter_gen` | POST | Generate letter usernames |
| `/api/genum` | POST | Generate number usernames |
| `/api/settings` | GET/POST | View/modify settings |
| `/api/clear_snipes` | POST | Clear in-memory list |
| `/api/export_available` | GET | Export as JSON |

---

## File Structure

```
ducksnipe/
├── ducksnipe.py              Main CLI application
├── web_server.py             Web interface server
├── config.py                 Configuration and wordlists
├── api.py                    Async API handling
├── commands.py               Command implementations
├── utils.py                  Utility functions
├── install.bat               Windows installer
├── start.bat                 Interactive launcher
├── templates/
│   └── index.html           Web UI
├── settings.json             Persisted settings
├── words.txt                 Custom wordlist
├── users.txt                 Saved accounts
├── available_usernames.txt   Found usernames
└── DuckSnipeLogs/            Operation logs
```

---

## Rate Limiting

### Default Configuration

Safe defaults prevent API throttling:
- 10 concurrent requests
- 0.3 second delay between batches
- Automatic rate limit detection

### If Rate Limited

1. Wait 5-10 minutes before retrying
2. Reduce concurrent requests to 5
3. Increase delay to 0.5 or 1.0 seconds
4. Check `DuckSnipeLogs/rate_limit_alerts.txt`

### Best Practices

- Begin with default settings
- Increase speed only if no throttling occurs
- Monitor rate limit logs regularly
- Batch large operations into smaller groups
- Use lower settings for mass checking (1000+ usernames)

---

## Troubleshooting

### Web Interface

**Flask Import Error**
```bash
pip install flask
```

**Templates Not Found**
Ensure `templates/index.html` exists in correct location.

**Port Conflict**
Edit `web_server.py` to change port:
```python
run_server(host='127.0.0.1', port=8081)
```

### CLI

**Rate Limiting (429/403)**
Lower concurrent requests and increase delay via settings menu.

**Import Errors**
```bash
pip install aiohttp colorama flask
```

**Permission Errors**
Check write permissions for DuckSnipeLogs folder.

### Installation

**Python Not Found**
Install Python 3.8+ from python.org with "Add to PATH" enabled.

**Virtual Environment Issues**
```bash
python -m venv venv --clear
```

---

## Advanced Usage

### Dual Mode Operation

Running CLI and Web simultaneously provides optimal workflow:
- Execute commands quickly via CLI
- Monitor results visually via Web
- Shared data between interfaces
- Independent operation of each interface

Launch via `start.bat → [3]` or manually:
```bash
# Terminal 1
python web_server.py

# Terminal 2
python ducksnipe.py
```

### Custom Port Configuration

Modify `web_server.py`:
```python
def run_server(host='127.0.0.1', port=8080):
```

Change `port` value to desired port number.

### Network Access

Default configuration restricts access to localhost. To enable network access:
```python
run_server(host='0.0.0.0', port=8080)
```

Warning: This exposes the interface to your network.

---

## Development

### Requirements

- Python 3.8+
- aiohttp 3.8.0+
- colorama 0.4.6+
- Flask 2.3.0+

### Setup

```bash
git clone https://github.com/daredjumper/ducksnipe.git
cd ducksnipe
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install aiohttp colorama flask
```

### Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes
4. Test both CLI and Web interfaces
5. Submit pull request

---

## Disclaimer

Educational purposes only.

- Uses public Roblox API for username validation
- Username sniping may violate Roblox Terms of Service
- Automated account creation is not supported and violates TOS
- Respect rate limits to avoid IP restrictions
- Use responsibly and ethically
- Developers assume no liability for misuse

Finding available usernames: Educational use  
Automated account creation: Prohibited

---

## License

MIT License - See LICENSE for details

---

## Resources

[Report Bug](https://github.com/daredjumper/ducksnipe/issues) • [Request Feature](https://github.com/daredjumper/ducksnipe/issues) • [Discussions](https://github.com/daredjumper/ducksnipe/discussions)

---

## Changelog

**Version 1.0.9**
- Added Flask-based web interface
- Added number generator (genum command)
- Added interactive launcher (start.bat)
- Added REST API endpoints
- Added JSON export functionality
- Added live statistics dashboard
- Updated installer for Flask support
- Improved error handling and logging
- Enhanced documentation

---

Made by the community for the community