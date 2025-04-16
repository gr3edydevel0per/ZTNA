import os
import subprocess
import logging
import requests
from pathlib import Path
import win32con

class WGManager:
    def __init__(self, uuid):
        self.uuid = uuid
        self.wg_path = r"C:\Program Files\WireGuard\wg.exe"
        self.wireguard_exe_path = r"C:\Program Files\WireGuard\wireguard.exe"
        self.config_dir = Path(os.path.expanduser("~")) / "Documents" / "owlguard"
        self.wg_server_public_key = self.config_dir / "wg_server_public_key"
        self.wg_client_public_key = self.config_dir / "wg_client_public_key"
        self.wg_client_private_key = self.config_dir / "wg_client_private_key"
        self.wg_config_file = self.config_dir / "wg.conf"

    def run_powershell(self, command):
        """Executes a PowerShell command and returns output or None on failure."""
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            return subprocess.check_output(
                ["powershell", "-Command", command],
                stderr=subprocess.DEVNULL,
                text=True,
                startupinfo=startupinfo,
                creationflags=win32con.CREATE_NO_WINDOW
            ).strip()
        except subprocess.CalledProcessError as e:
            logging.error(f"PowerShell command failed: {e}")
            return None

    def run_command(self, command_list):
        """Run EXE command using subprocess"""
        try:
            result = subprocess.run(
                command_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True,
                creationflags=win32con.CREATE_NO_WINDOW
            )
            print(f"[+] Command output:\n{result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[!] Command failed:\n{e.stderr}")
            return False

    def is_key_file_exists(self):
        return self.wg_client_private_key.exists() and self.wg_client_public_key.exists()

    def is_wireguard_server_key_file_exists(self):
        return self.wg_server_public_key.exists()

    def is_wireguard_installed(self):
        return os.path.exists(self.wg_path)

    def generate_client_keys(self):
        if self.is_key_file_exists():
            print("[+] Keys already generated.")
            return True

        self.config_dir.mkdir(parents=True, exist_ok=True)

        private_key = self.run_powershell("wg genkey")
        if private_key:
            with open(self.wg_client_private_key, 'w') as f:
                f.write(private_key)

            public_key = self.run_powershell(f"echo {private_key} | wg pubkey")
            if public_key:
                with open(self.wg_client_public_key, 'w') as f:
                    f.write(public_key)
                print("[+] WireGuard keys generated.")
                return True
        return False

    def get_wg_server_public_key(self):
        log_file = self.config_dir / f"{self.uuid}.log"
        try:
            with open(log_file, "r") as file:
                for line in file:
                    if "[setenv] [WG_PUBLIC_KEY]" in line:
                        key = line.split(" ")[3][1:-2]
                        print(f"[+] Found WG Server Key: {key}")
                        return key
        except Exception as e:
            logging.error(f"Error getting WG server public key: {str(e)}")
        return None

    def setup_wireguard_client(self):
        if not self.is_key_file_exists():
            if not self.generate_client_keys():
                print("[-] Failed to generate WireGuard keys.")
                return

            # Try fetching server public key from backend
            url = "http://owlguard.org/wgkey.php"
            try:
                response = requests.get(url, verify=False)
                if response.status_code == 200:
                    with open(self.wg_server_public_key, "w") as f:
                        f.write(response.text)
                    print("[+] WireGuard server key fetched and saved.")
                else:
                    print(f"[-] Failed to fetch server key. Status: {response.status_code}")
            except requests.RequestException as e:
                logging.error(f"HTTP error fetching server key: {str(e)}")

        if not self.is_wireguard_server_key_file_exists():
            wg_server_key = self.get_wg_server_public_key()
            if wg_server_key:
                with open(self.wg_server_public_key, "w") as f:
                    f.write(wg_server_key)
                print("[+] Server key extracted from log and saved.")
            else:
                print("[-] Could not retrieve WireGuard server public key.")

    def start_wireguard_service(self):
        if not self.wg_config_file.exists():
            print(f"[-] Config file does not exist: {self.wg_config_file}")
            return

        print(f"[+] Starting WireGuard tunnel using config: {self.wg_config_file}")
        cmd = [
            self.wireguard_exe_path,
            "/installtunnelservice",
            str(self.wg_config_file)
        ]
        self.run_command(cmd)

    def stop_wireguard_service(self):
        print("[+] Stopping WireGuard tunnel service...")
        cmd = [
            self.wireguard_exe_path,
            "/uninstalltunnelservice",
            "wg"  # Replace with your tunnel name if different
        ]
        self.run_command(cmd)

