from pydantic import BaseModel
from typing import Optional

class AuthConfig(BaseModel):
    auth_type: str = "none" # none, bearer, basic, oauth2
    token: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    token_url: Optional[str] = None
