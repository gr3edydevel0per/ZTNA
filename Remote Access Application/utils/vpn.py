import os
import subprocess
import logging

class VPNManager:
    def __init__(self):
        self.openvpn_path = r"C:\Program Files\OpenVPN Connect\OpenVPNConnect.exe"
        self.connector_path = r"C:\Program Files\OpenVPN Connect\ovpnconnector.exe"
        
    def is_openvpn_installed(self):
        """Check if OpenVPN is installed"""
        return os.path.exists(self.openvpn_path) and os.path.exists(self.connector_path)
    

    def install_service(self):
        """Install OpenVPN service"""
        subprocess.run([self.openvpn_path, "install"], shell=True)

    def start_vpn(self):
        """Start OpenVPN connection"""
        try:
            if not self.is_openvpn_installed():
                return {
                    "status": "error",
                    "message": "OpenVPN is not installed"
                }
            
            result = subprocess.run(
                [self.connector_path, "start"],
                capture_output=True,
                text=True,
                check=False  # Don't raise exception on non-zero return code
            )
            if "Failed to acquire service handle" in result.stdout:
                self.install_service()
                self.start_vpn()
            print (
                 result.stdout )
            
        except Exception as e:
            logging.error(f"Unexpected error starting VPN: {str(e)}")
            print(e)
    
    def stop_vpn(self):
        """Stop OpenVPN connection"""
        try:
            result = subprocess.run(
                [self.connector_path, "stop"],
                capture_output=True,
                text=True,
                check=False
            )
            
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
    
# Create a singleton instance
vpn_manager = VPNManager()

vpn_manager.start_vpn()
# Prop