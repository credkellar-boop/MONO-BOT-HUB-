import os
import json
import requests
from lib.github_app_client import GitHubAppClient # Fixed Path

def broadcast_halt(reason: str):
    """Sends a global halt signal to all 700+ worker bots."""
    client = GitHubAppClient(os.getenv("APP_ID"), "secrets/app-key.pem")
    token = client.get_installation_token(os.getenv("INSTALLATION_ID"))
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Use 'configs' folder and '.json' extension
    with open('configs/fleet_manifest.json', 'r') as f:
        fleet = json.load(f)

    for bot in fleet:
        repo_name = bot['full_name']
        url = f"https://api.github.com/repos/{repo_name}/dispatches"
        payload = {
            "event_type": "emergency_halt",
            "client_payload": {"reason": reason, "action": "STOP_IMMEDIATELY"}
        }
        requests.post(url, headers=headers, json=payload)
