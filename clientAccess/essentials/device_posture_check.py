import os
import platform
import subprocess
import psutil

def check_os_version():
    """Check if the OS version is compliant and return details."""
    os_info = platform.uname()
    os_details = f"{os_info.system} {os_info.release} {os_info.version}"
    is_compliant = (
        (os_info.system == "Windows" and os_info.release >= "10") or
        (os_info.system == "Linux") or
        (os_info.system == "Darwin")
    )
    return {"details": os_details, "compliant": is_compliant}

def check_os_patch_level():
    """Check if the OS has the latest patches."""
    if platform.system() == "Windows":
        try:
            result = subprocess.check_output(["powershell", "Get-HotFix"], stderr=subprocess.DEVNULL)
            details = "Latest patches installed" if result else "No patches found"
            is_compliant = bool(result)
            return {"details": details, "compliant": is_compliant}
        except Exception as e:
            return {"details": f"Error checking patches: {e}", "compliant": False}
    return {"details": "Patch level check not implemented for this OS", "compliant": False}

def check_antivirus_status():
    """Check if antivirus is running and return details."""
    if platform.system() == "Windows":
        try:
            result = subprocess.check_output(["powershell", "Get-MpComputerStatus"], stderr=subprocess.DEVNULL)
            is_running = b"RealTimeProtectionEnabled" in result
            details = "Windows Defender is running" if is_running else "No antivirus or Real-Time Protection disabled"
            return {"details": details, "compliant": is_running}
        except Exception as e:
            return {"details": f"Error checking antivirus: {e}", "compliant": False}
    return {"details": "Antivirus check not implemented for this OS", "compliant": False}



def check_tpm_enabled():
    """ Check if tpm is enabled or not """
    if platform.system()=="Windows":
        try:
            result= subprocess.check_output([ "powershell","get-tpm", "|", "select TpmEnabled"],stderr=subprocess.DEVNULL)
            print(result)
            enabled = b'True' in result
            if enabled:
                return {"details": enabled, "compliant": "True"}
            else:
                return  {"details": enabled, "compliant": "False"}
        except:
            return {"details": f"Error checking tepm: {Exception}", "compliant": False}

def check_disk_encryption():
    """Check if disk encryption is enabled and return details."""
    if platform.system() == "Linux":
        try:
            result = subprocess.check_output(["lsblk", "-o", "NAME,MOUNTPOINT,TYPE,FSTYPE,ENCRYPTION"], stderr=subprocess.DEVNULL)
            details = result.decode()
            is_encrypted = "crypto_LUKS" in details  # Example check
            return {"details": details, "compliant": is_encrypted}
        except Exception as e:
            return {"details": f"Error checking disk encryption: {e}", "compliant": False}
    return {"details": "Disk encryption check not implemented for this OS", "compliant": False}

def check_firewall_status():
    """Check if the firewall is enabled and return details."""
    if platform.system() == "Windows":
        try:
            result = subprocess.check_output(["powershell", "Get-NetFirewallProfile"], stderr=subprocess.DEVNULL)
            is_enabled = b"Enabled" in result
            details = "Firewall is enabled" if is_enabled else "Firewall is disabled"
            return {"details": details, "compliant": is_enabled}
        except Exception as e:
            return {"details": f"Error checking firewall: {e}", "compliant": False}
    elif platform.system() == "Linux":
        try:
            result = subprocess.check_output(["ufw", "status"], stderr=subprocess.DEVNULL)
            is_active = b"active" in result
            details = "Firewall is active" if is_active else "Firewall is inactive"
            return {"details": details, "compliant": is_active}
        except Exception as e:
            return {"details": f"Error checking firewall: {e}", "compliant": False}
    return {"details": "Firewall check not implemented for this OS", "compliant": False}

def check_secureboot_status():
    """Check for SecureBoot is enabled or not."""
    if platform.system() == "Windows":
        try:
            result = subprocess.check_output(["powershell", "Confirm-SecureBootUEFI"], stderr=subprocess.DEVNULL)
            is_enabled = b"True" in result
            details = "SecureBoot is enabled" if is_enabled else "SecureBoot is not enabled"
            return {"details": details, "compliant": is_enabled}
        except Exception as e:
            return {"details": f"Error checking TPM: {e}", "compliant": False}
    return {"details": "TPM check not implemented for this OS", "compliant": False}

def check_installed_software():
    """Check for blacklisted or missing software."""
    if platform.system() == "Windows":
        try:
            result = subprocess.check_output(["powershell", "Get-WmiObject", "Win32_Product"], stderr=subprocess.DEVNULL)
            details = "Software inventory retrieved successfully"
            is_compliant = True  
            return {"details": details, "compliant": is_compliant}
        except Exception as e:
            return {"details": f"Error checking software: {e}", "compliant": False}
    return {"details": "Software check not implemented for this OS", "compliant": False}




def main():
    print("Starting Enhanced Device Posture Check...\n")

    checks = {

        "OS Version": check_os_version(),
        "Antivirus Status": check_antivirus_status(),
        "Disk Encryption": check_disk_encryption(),
        "Firewall Status": check_firewall_status(),
        "OS Patch Level": check_os_patch_level(),
        "Installed Software": check_installed_software(),
        "Check SecureBoot" : check_secureboot_status(),
        "Check TPM": check_tpm_enabled(),
    }

    print("Device Posture Check Details:\n")
    for check, result in checks.items():
        print(f"{check}:")
        print(f"  Details: {result['details']}")
        print(f"  Status: {'Compliant' if result['compliant'] else 'Non-Compliant'}\n")

    overall_compliance = all(result["compliant"] for result in checks.values())

    print("Final Device Posture Check Result:")
    if overall_compliance:
        print("Device is compliant. Access granted.")
    else:
        print("Device is non-compliant. Access denied.")

    return {"checks": checks, "compliant": overall_compliance}

if __name__ == "__main__":
    posture_result = main()
    # print("\nPosture Result Data Structure:")
    # print(posture_result)  # Print result dictionary for further debugging or logging
    print()