import os
import json
import requests
from lib.github_app_client import GitHubAppClient

def broadcast_halt(reason: str):
    """Sends a global halt signal to all 700+ worker bots."""
    # Auth via Hub's GitHub App
    client = GitHubAppClient(os.getenv("APP_ID"), "secrets/app_key.pem")
    token = client.get_installation_token(os.getenv("INSTALLATION_ID"))
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Load manifest from configs/fleet_manifest.json
    with open('configs/fleet_manifest.json', 'r') as f:
        fleet = json.load(f)

    print(f"🛑 EMERGENCY HALT INITIATED: {reason}")
    
    for bot in fleet:
        repo_name = bot['full_name']
        url = f"https://api.github.com/repos/{repo_name}/dispatches"
        payload = {
            "event_type": "emergency_halt",
            "client_payload": {"reason": reason, "action": "STOP_IMMEDIATELY"}
        }
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 204:
            print(f"SUCCESS: Halt signal delivered to {repo_name}")
        else:
            print(f"FAILED: Could not reach {repo_name} - Status: {response.status_code}")

if __name__ == "__main__":
    broadcast_halt("Global System Update - Integrity Check 2026")
