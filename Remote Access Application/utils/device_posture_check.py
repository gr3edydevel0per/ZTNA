# File contains functions to check device posture

import subprocess
import platform

def run_powershell(command):
    try:
        result = subprocess.check_output(["powershell", "-Command", command], stderr=subprocess.DEVNULL, text=True)
        return result.strip()
    except subprocess.CalledProcessError:
        return "Error executing command"

def check_os_version():
    os_info = platform.uname()
    is_compliant = os_info.system == "Windows" and int(os_info.release.split('.')[0]) >= 10
    return {"details": f"{os_info.system} {os_info.release}", "compliant": is_compliant}

def check_antivirus_status():
    command = "Get-MpComputerStatus | Select-Object -ExpandProperty RealTimeProtectionEnabled"
    result = run_powershell(command)
    is_compliant = result == "True"
    return {"details": "Antivirus is running" if is_compliant else "Antivirus is disabled", "compliant": is_compliant}

def check_firewall_status():
    command = "Get-NetFirewallProfile | Select-Object -ExpandProperty Enabled"
    result = run_powershell(command)
    is_compliant = "True" in result
    return {"details": "Firewall is enabled" if is_compliant else "Firewall is disabled", "compliant": is_compliant}

def check_tpm_status():
        try:
            result = subprocess.check_output(["powershell", "get-tpm", "|", "select TpmEnabled"], stderr=subprocess.DEVNULL)
            enabled = b'True' in result
            return {"details": "TPM is enabled" if enabled else "TPM is disabled", "compliant": enabled}
        except Exception as e:
            return {"details": f"Error checking TPM: {e}", "compliant": False}
        return {"details": "TPM check not implemented for this OS", "compliant": False}


def check_secureboot_status():
    if platform.system() == "Windows":
        try:
            result = subprocess.check_output(["powershell", "Confirm-SecureBootUEFI"], stderr=subprocess.DEVNULL)
            is_enabled = b"True" in result
            return {"details": "SecureBoot is enabled" if is_enabled else "SecureBoot is not enabled", "compliant": is_enabled}
        except Exception as e:
            return {"details": f"Error checking SecureBoot: {e}", "compliant": False}
    return {"details": "SecureBoot check not implemented for this OS", "compliant": False}

def check_bitlocker_status():
    command = "(Get-BitLockerVolume).ProtectionStatus"
    result = run_powershell(command)
    is_compliant = "1" in result
    return {"details": "BitLocker is enabled" if is_compliant else "BitLocker is not enabled", "compliant": is_compliant}

def run_device_posture_check():
    checks = {
        "OS Version": check_os_version(),
        "Antivirus Status": check_antivirus_status(),
        "Firewall Status": check_firewall_status(),
        "TPM Status": check_tpm_status(),
       # "SecureBoot": check_secureboot_status()
       # "BitLocker Status": check_bitlocker_status()
    }
    print(checks)
    non_compliant_checks = {k: v for k, v in checks.items() if not v["compliant"]}
    
    if non_compliant_checks:
        print("Device is non-compliant. Issues detected:")
        for check, result in non_compliant_checks.items():
            print(f"{check}: {result['details']}")
    else:
        print("Device is fully compliant.")
    
    return {"checks": checks, "compliant": not bool(non_compliant_checks)}

