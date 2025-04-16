import platform
import socket
import uuid
import hashlib
import subprocess
import threading
import win32con
from core.utils.essentials import get_current_machine_id, get_ip


def get_device_data():
    """
    Collects device-specific data for authorization.
    """
    threads = []
    results = {}

    def collect_data(key, func):
        """Function to collect data and store it in the results dict."""
        results[key] = func()

    # Start threads for each data collection task
    threads.append(threading.Thread(target=collect_data, args=("public_ip", get_ip)))
    threads.append(threading.Thread(target=collect_data, args=("device_id", get_current_machine_id)))
    threads.append(threading.Thread(target=collect_data, args=("device_fingerprint", generate_device_id)))
    threads.append(threading.Thread(target=collect_data, args=("device_name", socket.gethostname)))
    threads.append(threading.Thread(target=collect_data, args=("device_type", get_device_type)))
    threads.append(threading.Thread(target=collect_data, args=("device_os", get_device_os)))
    threads.append(threading.Thread(target=collect_data, args=("hardware_fingerprint", get_hardware_id)))

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return results





def get_command_output( command):       
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            return subprocess.check_output(
                command,
                stderr=subprocess.DEVNULL,
                text=True,
                startupinfo=startupinfo,
                creationflags=win32con.CREATE_NO_WINDOW
            ).strip()
        except subprocess.CalledProcessError:
            return None

def get_command_output(command):
    """Executes a system command and returns its output."""
    try:
        return subprocess.check_output(command, shell=True).decode().strip()
    except subprocess.CalledProcessError:
        return ""


def generate_device_id():
    """
    Generates a unique device identifier by hashing system and hardware details.
    """
    identifiers = [
        get_system_info(),
        platform.node(),
        platform.machine(),
        platform.system(),
        str(uuid.getnode()),
        socket.gethostname()
    ]
    
    identifiers = list(filter(None, identifiers))
    return hashlib.sha256(''.join(identifiers).encode()).hexdigest()


def get_system_info():
    """Retrieves the MAC Address, CPU ID, and Disk Serial Number."""
    system = platform.system()
    
    # Create threads for each system information gathering function
    mac_address = get_mac_address(system)
    cpu_id = get_cpu_id(system)
    disk_serial = get_disk_serial(system)

    return ''.join([mac_address, cpu_id, disk_serial])


def get_mac_address(system):
    """Retrieves the MAC address based on the system type."""
    return get_command_output('getmac /v /fo csv').split('\n')[1].split(',')[0].strip('"')


def get_cpu_id(system):
    """Retrieves the CPU ID based on the system type."""
    return get_command_output('wmic cpu get ProcessorId').split('\n')[1]

def get_disk_serial(system):
    """Retrieves the Disk Serial Number based on the system type."""
    return get_command_output('wmic diskdrive get SerialNumber').split('\n')[1]


def get_device_type():
    """Determines whether the device is a laptop or desktop."""
    chassis = get_command_output('wmic systemenclosure get chassistypes')
    return "laptop" if any(str(x) in chassis for x in [9, 10, 14]) else "desktop"


def get_device_os():
    """Retrieves the detailed OS information."""
    return f"{platform.system()} {platform.release()} ({platform.version()})"


def get_hardware_id():
    """
    Retrieves a hashed identifier based on BIOS serial and other hardware info.
    """
    system = platform.system()
    hardware_info = get_command_output(
        'wmic bios get serialnumber'
    )
    return hashlib.sha256(hardware_info.encode()).hexdigest() if hardware_info else None

