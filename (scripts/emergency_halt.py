import os
import requests
import json
from lib.github_app_client import GitHubAppClient

def broadcast_halt():
    client = GitHubAppClient(os.getenv("APP_ID"), "secrets/app-private-key.pem")
    token = client.get_installation_token(os.getenv("INSTALLATION_ID"))
    headers = {"Authorization": f"token {token}"}

    with open('configs/fleet_manifest.json', 'r') as f:
        repos = json.load(f)

    for repo in repos:
        url = f"https://api.github.com/repos/{repo['full_name']}/dispatches"
        payload = {
            "event_type": "emergency_halt",
            "client_payload": {"reason": "Global Security Update", "action": "STOP"}
        }
        r = requests.post(url, headers=headers, json=payload)
        print(f"Halt Signal -> {repo['full_name']}: {r.status_code}")

if __name__ == "__main__":
    broadcast_halt()
