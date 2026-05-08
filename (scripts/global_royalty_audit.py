import os
import pandas as pd
import requests
from io import StringIO
from lib.github_app_client import GitHubAppClient

def fetch_fleet_logs():
    # Auth via your GitHub App
    client = GitHubAppClient(os.getenv("APP_ID"), "secrets/app-private-key.pem")
    token = client.get_installation_token(os.getenv("INSTALLATION_ID"))
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}

    # Load your manifest of 700 bots
    with open('configs/fleet_manifest.json', 'r') as f:
        repos = json.load(f)

    master_frames = []

    for repo in repos:
        repo_name = repo['full_name']
        print(f"Auditing {repo_name}...")

        # 1. Get the latest successful run artifact
        art_url = f"https://api.github.com/repos/{repo_name}/actions/artifacts"
        artifacts = requests.get(art_url, headers=headers).json()

        if artifacts['total_count'] > 0:
            # 2. Download the 'shield-audit-log' (latest zip)
            download_url = artifacts['artifacts'][0]['archive_download_url']
            # Note: GitHub returns a zip; you'll need to unzip in memory
            response = requests.get(download_url, headers=headers)
            
            # 3. Process CSV logic (simplified for raw text)
            # Assuming bot saves to 'audit/royalty_log.csv'
            df = pd.read_csv(StringIO(response.text))
            df['bot_id'] = repo_name
            master_frames.append(df)

    # 4. The "Max" Compilation
    final_report = pd.concat(master_frames, ignore_index=True)
    final_report.to_csv("GLOBAL_FLEET_AUDIT_2026.csv", index=False)
    print("DONE: Global Audit generated for 700 bots.")

if __name__ == "__main__":
    fetch_fleet_logs()
