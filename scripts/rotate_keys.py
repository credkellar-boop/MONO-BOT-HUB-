import os
import json
from lib.github_app_client import GitHubAppClient
from nacl import encoding, public # For encrypting secrets

def encrypt_secret(public_key: str, secret_value: str) -> str:
    """Encrypts a Unicode string using a public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return encoding.Base64Encoder().encode(encrypted).decode("utf-8")

def update_fleet_secrets(secret_name, secret_value):
    client = GitHubAppClient(os.getenv("APP_ID"), "secrets/app-private-key.pem")
    token = client.get_installation_token(os.getenv("INSTALLATION_ID"))
    
    with open('configs/fleet_manifest.json', 'r') as f:
        repos = json.load(f)

    for repo in repos:
        repo_name = repo['full_name']
        print(f"Updating secret {secret_name} for {repo_name}...")
        
        # 1. Get Repo Public Key
        pk_url = f"https://api.github.com/repos/{repo_name}/actions/secrets/public-key"
        headers = {"Authorization": f"token {token}"}
        pk_data = requests.get(pk_url, headers=headers).json()
        
        # 2. Encrypt and Upload
        encrypted_val = encrypt_secret(pk_data['key'], secret_value)
        put_url = f"https://api.github.com/repos/{repo_name}/actions/secrets/{secret_name}"
        data = {"encrypted_value": encrypted_val, "key_id": pk_data['key_id']}
        requests.put(put_url, headers=headers, json=data)

if __name__ == "__main__":
    update_fleet_secrets("MONAD_RPC_URL", "https://your-dedicated-node.com")
