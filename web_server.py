"""
DuckSnipe Web Server
Flask-based web interface for DuckSnipe
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import asyncio
import os
from datetime import datetime
import json

import config
from api import validate_usernames_concurrent
from utils import safe_file_read, safe_file_write, sync_custom_words, log_message
from commands import generate_random_username

app = Flask(__name__)

# Store active checking status
checking_status = {
    "is_checking": False,
    "current_progress": 0,
    "total_usernames": 0,
    "found_available": 0
}

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html', version=config.VERSION)

@app.route('/api/stats')
def get_stats():
    """Get current statistics"""
    available_content = safe_file_read(config.AVAILABLE_FILE)
    available_count = len(available_content.strip().split('\n')) if available_content and available_content.strip() else 0
    
    accounts_content = safe_file_read(config.USERS_FILE)
    accounts_count = len(accounts_content.strip().split('\n')) if accounts_content and accounts_content.strip() else 0
    
    return jsonify({
        "available_count": available_count,
        "accounts_count": accounts_count,
        "in_memory_snipes": len(config.AVAILABLE_SNIPES),
        "custom_words": len(config.CUSTOM_WORDS),
        "settings": {
            "max_concurrent": config.MAX_CONCURRENT_REQUESTS,
            "request_delay": config.REQUEST_DELAY
        }
    })

@app.route('/api/available')
def get_available():
    """Get list of available usernames"""
    content = safe_file_read(config.AVAILABLE_FILE)
    if not content or not content.strip():
        return jsonify({"usernames": []})
    
    lines = content.strip().split('\n')
    usernames = []
    for line in lines:
        # Parse "[timestamp] username" format
        if ']' in line:
            parts = line.split(']', 1)
            if len(parts) == 2:
                timestamp = parts[0].replace('[', '').strip()
                username = parts[1].strip()
                usernames.append({"timestamp": timestamp, "username": username})
    
    return jsonify({"usernames": usernames})

@app.route('/api/check', methods=['POST'])
def check_usernames():
    """Check usernames for availability"""
    data = request.json
    usernames = data.get('usernames', [])
    
    if not usernames:
        return jsonify({"error": "No usernames provided"}), 400
    
    # Run async validation
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(validate_usernames_concurrent(usernames, "web_check"))
    loop.close()
    
    return jsonify({
        "success": True,
        "checked": len(usernames),
        "available": len(config.AVAILABLE_SNIPES)
    })

@app.route('/api/genkey', methods=['POST'])
def generate_key():
    """Generate usernames using genkey method"""
    data = request.json
    key_type = data.get('type', 'wordlist')
    key_val = data.get('key', '')
    
    if not key_val:
        return jsonify({"error": "Key value required"}), 400
    
    sources = {
        "wordlist": config.WORDLIST,
        "studio": config.RBXSTUDIO,
        "minerals": config.MINERALS,
        "custom": config.CUSTOM_WORDS,
        "great": config.GREATNAME,
        "jobs": config.JOBLIST
    }
    
    if key_type not in sources:
        return jsonify({"error": f"Invalid type: {key_type}"}), 400
    
    source = sources[key_type]
    if not source:
        return jsonify({"error": f"Empty wordlist: {key_type}"}), 400
    
    usernames = []
    for word in source:
        usernames.append(f"{key_val}{word}")
        usernames.append(f"{word}{key_val}")
    
    # Run async validation
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(validate_usernames_concurrent(usernames, "web_genkey"))
    loop.close()
    
    return jsonify({
        "success": True,
        "generated": len(usernames),
        "available": len(config.AVAILABLE_SNIPES)
    })

@app.route('/api/letter_gen', methods=['POST'])
def letter_gen():
    """Generate random letter usernames"""
    data = request.json
    length = data.get('length', 5)
    count = data.get('count', 100)
    include_numbers = data.get('include_numbers', True)
    
    if not (3 <= length <= 20):
        return jsonify({"error": "Length must be between 3 and 20"}), 400
    
    if not (1 <= count <= 50000):
        return jsonify({"error": "Count must be between 1 and 50000"}), 400
    
    usernames = set()
    max_attempts = count * 3
    attempts = 0
    
    while len(usernames) < count and attempts < max_attempts:
        username = generate_random_username(length, include_numbers)
        usernames.add(username)
        attempts += 1
    
    usernames = list(usernames)
    
    # Run async validation
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(validate_usernames_concurrent(usernames, "web_letter_gen"))
    loop.close()
    
    return jsonify({
        "success": True,
        "generated": len(usernames),
        "available": len(config.AVAILABLE_SNIPES)
    })

@app.route('/api/genum', methods=['POST'])
def genum():
    """Generate number-based usernames"""
    data = request.json
    gen_type = data.get('type', '1')
    digits = data.get('digits', 5)
    count = data.get('count', 100)
    prefix = data.get('prefix', '')
    suffix = data.get('suffix', '')
    start_num = data.get('start_num', 0)
    end_num = data.get('end_num', 100)
    
    usernames = []
    
    if gen_type == '4':  # Sequential
        count = min(end_num - start_num + 1, 50000)
        usernames = [str(num) for num in range(start_num, start_num + count)]
    else:
        # Validate length
        prefix_suffix_length = len(prefix) + len(suffix)
        if prefix_suffix_length + digits > 20:
            return jsonify({"error": "Total length exceeds 20 characters"}), 400
        
        if not (1 <= digits <= 10):
            return jsonify({"error": "Digits must be between 1 and 10"}), 400
        
        if not (1 <= count <= 50000):
            return jsonify({"error": "Count must be between 1 and 50000"}), 400
        
        # Generate random numbers
        import random
        usernames_set = set()
        max_attempts = count * 3
        attempts = 0
        
        min_num = 10 ** (digits - 1) if digits > 1 else 0
        max_num = (10 ** digits) - 1
        
        while len(usernames_set) < count and attempts < max_attempts:
            num = random.randint(min_num, max_num)
            username = f"{prefix}{num}{suffix}"
            usernames_set.add(username)
            attempts += 1
        
        usernames = list(usernames_set)
    
    # Run async validation
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(validate_usernames_concurrent(usernames, "web_genum"))
    loop.close()
    
    return jsonify({
        "success": True,
        "generated": len(usernames),
        "available": len(config.AVAILABLE_SNIPES)
    })

@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    """Get or update settings"""
    if request.method == 'GET':
        return jsonify({
            "max_concurrent_requests": config.MAX_CONCURRENT_REQUESTS,
            "request_delay": config.REQUEST_DELAY,
            "log_folder": config.LOG_FOLDER,
            "users_file": config.USERS_FILE,
            "words_file": config.WORDS_FILE,
            "available_file": config.AVAILABLE_FILE
        })
    else:
        data = request.json
        
        if 'max_concurrent_requests' in data:
            val = int(data['max_concurrent_requests'])
            if 1 <= val <= 100:
                config.MAX_CONCURRENT_REQUESTS = val
        
        if 'request_delay' in data:
            val = float(data['request_delay'])
            if 0 <= val <= 10:
                config.REQUEST_DELAY = val
        
        # Save settings
        from utils import save_settings
        save_settings()
        
        return jsonify({"success": True})

@app.route('/api/clear_snipes', methods=['POST'])
def clear_snipes():
    """Clear in-memory available snipes"""
    count = len(config.AVAILABLE_SNIPES)
    config.AVAILABLE_SNIPES.clear()
    return jsonify({"success": True, "cleared": count})

@app.route('/api/export_available', methods=['GET'])
def export_available():
    """Export available usernames as JSON"""
    content = safe_file_read(config.AVAILABLE_FILE)
    if not content or not content.strip():
        return jsonify({"usernames": []})
    
    lines = content.strip().split('\n')
    usernames = []
    for line in lines:
        if ']' in line:
            parts = line.split(']', 1)
            if len(parts) == 2:
                timestamp = parts[0].replace('[', '').strip()
                username = parts[1].strip()
                usernames.append({"timestamp": timestamp, "username": username})
    
    return jsonify({"usernames": usernames, "export_date": datetime.now().isoformat()})

def run_server(host='127.0.0.1', port=8080):
    """Start the web server"""
    print(f"\n🌐 DuckSnipe Web UI starting on http://{host}:{port}")
    print(f"📊 Open your browser to access the dashboard")
    print(f"⚡ Press Ctrl+C to stop the server\n")
    app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    run_server()