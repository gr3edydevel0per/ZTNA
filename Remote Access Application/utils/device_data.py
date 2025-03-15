# File contains functions to get device data for device authorization

import platform
import socket
import uuid
import hashlib
import os
import subprocess

def get_device_data():
    """
    Get device data from the device including a unique identifier
    """
    device_data = {
        "device_id": generate_device_id(),
        "device_name": get_device_name(),
        "device_type": get_device_type(),
        "device_os": get_device_os(),
        "hardware_id": get_hardware_id()
    }
    return device_data

def generate_device_id():
    """
    Generates a unique device identifier based on hardware and system information.
    Combines multiple factors to create a persistent identifier.
    """
    identifiers = []
    
    try:
        if platform.system() == "Windows":
            mac = subprocess.check_output('getmac /v /fo csv').decode()
            mac = mac.split('\n')[1].split(',')[0].strip('"')
        elif platform.system() == "Linux":
            mac = subprocess.check_output(['ifconfig']).decode()
            mac = mac.split('ether')[1].split()[0]
        else:
            mac = subprocess.check_output(['ifconfig']).decode()
            mac = mac.split('ether')[1].split()[0]
        
        if mac:
            identifiers.append(mac)
    except:
        try:
            mac = uuid.getnode()
            identifiers.append(str(mac))
        except:
            pass

    try:
        if platform.system() == "Windows":
            cpu_id = subprocess.check_output('wmic cpu get ProcessorId').decode().split('\n')[1].strip()
        elif platform.system() == "Linux":
            with open('/proc/cpuinfo', 'r') as f:
                cpu_id = [line.split(':')[1].strip() for line in f.readlines() if 'Serial' in line][0]
        else:
            cpu_id = subprocess.check_output(['sysctl', '-n', 'machdep.cpu.brand_string']).decode().strip()
        identifiers.append(cpu_id)
    except:
        identifiers.append(platform.processor())

    try:
        if platform.system() == "Windows":
            disk_serial = subprocess.check_output('wmic diskdrive get SerialNumber').decode().split('\n')[1].strip()
        elif platform.system() == "Linux":
            disk_serial = subprocess.check_output(['udevadm', 'info', '--query=property', '--name=/dev/sda']).decode()
        else:
            disk_serial = subprocess.check_output(['system_profiler', 'SPHardwareDataType']).decode()
        identifiers.append(disk_serial)
    except:
        pass

    identifiers.extend([
        platform.node(),
        platform.machine(),
        platform.system(),
        str(uuid.getnode()),
        socket.gethostname()
    ])

    identifier_string = ''.join(identifiers)
    return hashlib.sha256(identifier_string.encode()).hexdigest()

def get_device_name():
    """Get the device name/hostname"""
    return socket.gethostname()

def get_device_type():
    """
    Attempt to determine the device type based on system information
    """
    system = platform.system()
    if system == "Windows":
        try:
            chassis = subprocess.check_output('wmic systemenclosure get chassistypes').decode()
            # ChassisTypes values: 9=Laptop, 3=Desktop, 4=Low Profile Desktop, 
            # 6=Mini Tower, 7=Tower, 10=Notebook, 14=Sub Notebook
            if any(str(x) in chassis for x in [9, 10, 14]):
                return "laptop"
            return "desktop"
        except:
            return "desktop"
    elif system == "Linux":
        try:
            with open('/sys/class/dmi/id/chassis_type', 'r') as f:
                chassis_type = int(f.read().strip())
                if chassis_type in [9, 10, 14]:
                    return "laptop"
                return "desktop"
        except:
            return "desktop"
    elif system == "Darwin":  # MacOS
        try:
            model = subprocess.check_output(['sysctl', '-n', 'hw.model']).decode().strip()
            if 'book' in model.lower():
                return "laptop"
            return "desktop"
        except:
            return "desktop"
    return "desktop"

def get_device_os():
    """Get detailed OS information"""
    system = platform.system()
    version = platform.version()
    release = platform.release()
    return f"{system} {release} ({version})"

def get_hardware_id():
    """
    Get additional hardware-specific identifiers
    """
    hardware_info = []
    
    try:
        # Get BIOS serial
        if platform.system() == "Windows":
            bios = subprocess.check_output('wmic bios get serialnumber').decode().strip()
            hardware_info.append(bios)
        elif platform.system() == "Linux":
            try:
                with open('/sys/class/dmi/id/product_uuid', 'r') as f:
                    hardware_info.append(f.read().strip())
            except:
                pass
    except:
        pass

    # Hash the combined hardware info
    hardware_string = ''.join(filter(None, hardware_info))
    if hardware_string:
        return hashlib.sha256(hardware_string.encode()).hexdigest()
    return None

def verify_device_trust(stored_id):
    """
    Verify if the current device matches the stored trusted device ID
    """
    current_device_id = generate_device_id()
    return current_device_id == stored_id


print(get_device_data())