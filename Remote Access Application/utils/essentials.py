
# File contains essential functions

import  requests
import subprocess



def getIP():
    endpoint = 'https://ipinfo.io/json'
    response = requests.get(endpoint, verify = True)

    if response.status_code != 200:
        return 'Status:', response.status_code, 'Not Connected To Internet. Please check your connection'
        exit()

    data = response.json()

    return data['ip']

def get_current_machine_id():
    return str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()