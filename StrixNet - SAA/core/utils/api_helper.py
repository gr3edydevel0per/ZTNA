import requests

def api_request(url, method='POST', json=None, headers=None):
    try:
        response = requests.request(method, url, json=json, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
