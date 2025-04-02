import subprocess
import platform
import time
from concurrent.futures import ThreadPoolExecutor
import win32con

class DevicePostureChecker:
    def __init__(self):
        self.results = {}

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
        except subprocess.CalledProcessError:
            return None

    def check_os_version(self):
        """Checks if the OS version is Windows 10 or later."""
        os_info = platform.uname()
        compliant = os_info.system == "Windows" and int(os_info.release.split('.')[0]) >= 10
        return {"details": f"{os_info.system} {os_info.release}", "compliant": compliant}

    def check_antivirus_status(self):
        """Checks if Windows Defender real-time protection is enabled."""
        result = self.run_powershell("Get-MpComputerStatus | Select-Object -ExpandProperty RealTimeProtectionEnabled")
        compliant = result == "True"
        return {"details": "Antivirus is running" if compliant else "Antivirus is disabled", "compliant": compliant}

    def check_firewall_status(self):
        """Checks if Windows Firewall is enabled."""
        result = self.run_powershell("Get-NetFirewallProfile | Select-Object -ExpandProperty Enabled")
        compliant = "True" in result if result else False
        return {"details": "Firewall is enabled" if compliant else "Firewall is disabled", "compliant": compliant}

    def check_tpm_status(self):
        """Checks if TPM is enabled."""
        result = self.run_powershell("(Get-Tpm).TpmEnabled")
        compliant = result == "True"
        return {"details": "TPM is enabled" if compliant else "TPM is disabled", "compliant": compliant}

    def check_secureboot_status(self):
        """Checks if Secure Boot is enabled."""
        if platform.system() == "Windows":
            result = self.run_powershell("Confirm-SecureBootUEFI")
            compliant = result == "True"
            return {"details": "SecureBoot is enabled" if compliant else "SecureBoot is not enabled", "compliant": compliant}
        return {"details": "SecureBoot check not implemented for this OS", "compliant": False}

    def check_bitlocker_status(self):
        """Checks if BitLocker is enabled."""
        result = self.run_powershell("(Get-BitLockerVolume).ProtectionStatus")
        compliant = result == "1"
        return {"details": "BitLocker is enabled" if compliant else "BitLocker is not enabled", "compliant": compliant}

    def run_device_posture_check(self):
        """Runs all posture checks concurrently and measures performance."""
        functions = {
            "OS Version": self.check_os_version,
            "Antivirus Status": self.check_antivirus_status,
            "Firewall Status": self.check_firewall_status,
            "TPM Status": self.check_tpm_status,
            "SecureBoot": self.check_secureboot_status,
            #"BitLocker Status": self.check_bitlocker_status,
        }

        # Run all checks concurrently using ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            future_to_check = {executor.submit(func): name for name, func in functions.items()}
            for future in future_to_check:
                check_name = future_to_check[future]
                start_time = time.time()
                result = future.result()  # Get the function output
                execution_time = time.time() - start_time
                self.results[check_name] = {**result, "execution_time": execution_time}

        non_compliant_checks = {k: v for k, v in self.results.items() if not v["compliant"]}
        if non_compliant_checks:
            print("\nDevice is non-compliant. Issues detected:")
            for check, result in non_compliant_checks.items():
                print(f"{check}: {result['details']}")
        else:
            print("\nDevice is fully compliant.")

        return {"checks": self.results, "compliant": not bool(non_compliant_checks)}


