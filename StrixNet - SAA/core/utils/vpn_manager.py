import os
import subprocess
import logging
import requests
from pathlib import Path
import time
import win32con
from core.utils.essentials import get_ip

class VPNManager:
    def __init__(self, uuid, session_token):
        self.openvpn_path = r"C:\Program Files\OpenVPN Connect\OpenVPNConnect.exe"
        self.connector_path = r"C:\Program Files\OpenVPN Connect\ovpnconnector.exe"
        self.config_dir = Path(os.path.expanduser("~")) / "Documents" / "owlguard"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.uuid = uuid
        self.ip_address = get_ip()
        self.config_path = self.config_dir / f"{self.uuid}.bmers.cache.ovpn"
        self.session_token = session_token
        self.device_data = self.session_token.get('device_data')
        self.device_id = self.device_data['device_id']
        self.device_fingerprint = self.device_data['device_fingerprint']
        self.device_os = self.device_data['device_os']
        self.device_name = self.device_data['device_name']
        self.device_type = self.device_data['device_type']
        self.hardware_fingerprint = self.device_data['hardware_fingerprint']

    def is_openvpn_installed(self):
        """Check if OpenVPN is installed"""
        return os.path.exists(self.openvpn_path) and os.path.exists(self.connector_path)
    
    def run_subprocess(self, command, shell=True, capture_output=True):
        """Helper method to run subprocess commands with hidden window"""
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        return subprocess.run(
            command,
            shell=shell,
            capture_output=capture_output,
            text=True,
            startupinfo=startupinfo,
            creationflags=win32con.CREATE_NO_WINDOW
        )

    def append_device_info_to_config(self):
        """Appends device details to the OpenVPN config file."""
        try:
            with open(self.config_path, "a") as file:
                file.write(f"\nsetenv UV_TOKEN {self.session_token.get('token')}\n")
                file.write(f"\nsetenv UV_UID {self.uuid}\n")
                file.write(f"\nsetenv UV_DEVICE_ID {self.device_id}\n")
                file.write(f"setenv UV_DEVICE_FINGERPRINT {self.device_fingerprint}\n")
                file.write(f"setenv UV_DEVICE_OS {self.device_os}\n")
                file.write(f"setenv UV_DEVICE_NAME {self.device_name}\n")
                file.write(f"setenv UV_DEVICE_TYPE {self.device_type}\n")
                file.write(f"setenv UV_HARDWARE_FINGERPRINT {self.hardware_fingerprint}\n")
                file.write(f"setenv UV_IP_ADDRESS {self.ip_address}\n")
            print("✅ Device details appended to OpenVPN config.")
        except Exception as e:
            print(f"❌ Error updating OpenVPN config: {e}")


    def remove_device_info_from_config(self):
        """
        Removes setenv lines (device details) from the OpenVPN config file.
        """
        try:
            if not os.path.exists(self.config_path):
                print("❌ Config file not found.")
                return
            
            with open(self.config_path, "r") as file:
                lines = file.readlines()

            with open(self.config_path, "w") as file:
                for line in lines:
                    if not line.startswith("setenv UV_"):
                        file.write(line)

            print("✅ Removed device details from OpenVPN config.")
        except Exception as e:
            print(f"❌ Error while cleaning OpenVPN config: {e}")








    def setup_service(self):
        """Install OpenVPN service and set configuration"""
        if not self.is_openvpn_installed():
            return {
                "status": "error",
                "message": "OpenVPN is not installed"
            }
        try:
            # Install service
            install_service = self.run_subprocess([self.connector_path, "install"])
            if install_service.returncode != 0:
                return {
                    "status": "error",
                    "message": "Failed to install OpenVPN service",
                    "details": install_service.stderr or "Unknown error occurred"
                }

            # Set config
            log_file = self.config_dir / f"{self.uuid}.log"
            set_config = self.run_subprocess([self.connector_path, "set-config", "profile", str(self.config_path)])
            if set_config.returncode != 0:
                return {
                    "status": "error",
                    "message": "Failed to set OpenVPN config",
                    "details": set_config.stderr or "Unknown error occurred"
                }

            # Set log file
            set_log_file = self.run_subprocess([self.connector_path, "set-config", "log", str(log_file)])
            if set_log_file.returncode != 0:
                return {
                    "status": "error",
                    "message": "Failed to set log file",
                    "details": set_log_file.stderr or "Unknown error occurred"
                }
            
            return {
                "status": "success",
                "message": "OpenVPN service setup completed successfully",
                "details": set_config.stdout
            }

        except Exception as e:
            logging.error(f"Error setting up OpenVPN service: {str(e)}")
            return {
                "status": "error",
                "message": "Failed to setup OpenVPN service",
                "details": str(e)
            }


        

    def start_vpn(self):
        """Start OpenVPN connection"""
        try:
            if not self.is_openvpn_installed():
                return {
                    "status": "error",
                    "message": "OpenVPN is not installed"
                }

            set_config = self.run_subprocess([self.connector_path, "set-config", str(self.config_path)])
            if set_config.returncode != 0:
                return {
                    "status": "error",
                    "message": "Failed to set OpenVPN config",
                    "details": set_config.stderr or "Unknown error occurred"
                }

            self.append_device_info_to_config()
            result = self.run_subprocess([self.connector_path, "start"])
            
            if "Failed to acquire service handle" in result.stdout:
                # Setup service if not already installed
                service_result = self.setup_service()
                if service_result["status"] == "error":
                    return service_result
                # Try starting VPN again after service setup
                result = self.run_subprocess([self.connector_path, "start"])
            
            if result.returncode != 0:
                return {
                    "status": "error",
                    "message": "Failed to start VPN connection",
                    "details": result.stderr or "Unknown error occurred"
                }
            
            return {
                "status": "success",
                "message": "VPN connection started",
                "details": result.stdout
            }
            
        except Exception as e:
            logging.error(f"Unexpected error starting VPN: {str(e)}")
            return {
                "status": "error",
                "message": "Failed to start VPN connection",
                "details": str(e)
            }
    
    def clear_logs(self):
        log_file = self.config_dir / f"{self.uuid}.log"
        if os.path.exists(log_file):
            os.remove(log_file)
        # create a new log file
        with open(log_file, "w") as file:
            file.write("")


    def get_private_ip(self):
        """Get private IP address from log file"""
        # from this line : netsh interface ip set address 3 static 10.0.8.2 255.255.255.0 gateway=10.0.8.1 store=active
        # get the ip address
        # wait for 4 seconds
        time.sleep(4)
        try:
            with open(self.config_dir / f"{self.uuid}.log", "r") as file:
                lines = file.readlines()
                for line in lines:
                    if "netsh interface ip set address" in line:
                        return line.split(" ")[7]
        except Exception as e:
            logging.error(f"Error getting private IP: {str(e)}")
            return None

    def stop_vpn(self):
        """Stop OpenVPN connection"""
        try:
            result = self.run_subprocess([self.connector_path, "stop"])
            self.remove_device_info_from_config()
            self.clear_logs()
            if result.returncode != 0:
                return {
                    "status": "error",
                    "message": "Failed to stop VPN connection",
                    "details": result.stderr or "Unknown error occurred"
                }
            
            return {
                "status": "success",
                "message": "VPN connection stopped",
                "details": result.stdout
            }
        except Exception as e:
            logging.error(f"Error stopping VPN: {str(e)}")
            return {
                "status": "error",
                "message": "Failed to stop VPN connection",
                "details": str(e)
            }



