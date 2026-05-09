import time
import jwt
import requests
import os

class GitHubAppClient:
    def __init__(self, app_id, private_key_path):
        self.app_id = app_id
        with open(private_key_path, 'r') as f:
            self.private_key = f.read()

    def _generate_jwt(self):
        payload = {
            "iat": int(time.time()),
            "exp": int(time.time()) + (10 * 60),
            "iss": self.app_id,
        }
        return jwt.encode(payload, self.private_key, algorithm="RS256")

    def get_installation_token(self, installation_id):
        jwt_token = self._generate_jwt()
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()["token"]
