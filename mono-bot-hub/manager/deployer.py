import os
import csv
import requests
import asyncio

# GitHub App Token injected via Actions Secret
GH_TOKEN = os.getenv("GH_APP_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {GH_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

async def dispatch_update(session, repo_name, bot_id):
    """Triggers the 'Update' workflow on a child bot."""
    url = f"https://api.github.com/repos/YourOrg/{repo_name}/dispatches"
    payload = {"event_type": "fleet_update", "client_payload": {"bot_id": bot_id}}
    
    async with session.post(url, headers=HEADERS, json=payload) as response:
        if response.status == 204:
            print(f"SUCCESS: Update dispatched to {repo_name}")
        else:
            print(f"FAILED: {repo_name} - {response.status}")

async def deploy_to_fleet():
    import aiohttp
    async with aiohttp.ClientSession() as session:
        tasks = []
        with open('../configurations/fleet-manifest.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Fire off concurrent updates for the Max speed
                tasks.append(dispatch_update(session, row['Repo_URL'], row['BotID']))
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(deploy_to_fleet())
qq
