import requests
from src.config import global_settings


class GoogleOAuthService:
    def __init__(self):
        self.client_id = global_settings.GG_CLIENT
        self.client_secret = global_settings.GG_SECRET
        self.redirect_uri = global_settings.GG_REDIRECT_URI
        self.token_url = "https://oauth2.googleapis.com/token"
        self.user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"

    async def get_user_info(self, code:str) -> dict:
        payload = {
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }
        token_response = await requests.post(self.token_url, data=payload).json()
        access_token = token_response.get('access_token')
        if not access_token:
            raise ValueError("Failed to obtain access token from Google")
        user_info_response = await requests.get(
            self.user_info_url,
            headers={'Authorization': f'Bearer {access_token}'}
        ).json()
        return user_info_response