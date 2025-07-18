from dataclasses import dataclass

@dataclass
class RefreshToken:
    token_id: str
    user_id: str
    refresh_token: str