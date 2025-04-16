# File contains essential functions

import requests
import subprocess
import platform

def get_ip():
    endpoint = 'https://ipinfo.io/json'
    response = requests.get(endpoint, verify=True)

    if response.status_code != 200:
        return f"Status: {response.status_code}, Not Connected To Internet. Please check your connection"
    
    data = response.json()
    return data.get('ip', 'Unknown IP')

def get_current_machine_id():
    if platform.system() == "Windows":
        return str(subprocess.check_output('wmic csproduct get uuid', shell=True), 'utf-8').split('\n')[1].strip()
    elif platform.system() == "Linux":
        return str(subprocess.check_output('cat /var/lib/dbus/machine-id', shell=True), 'utf-8').strip()
    else:
        return "Unsupported OS"


def download_file(url, destination):    
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
        return f"File downloaded to {destination}"
    else:
        return f"Failed to download file: {response.status_code}"
