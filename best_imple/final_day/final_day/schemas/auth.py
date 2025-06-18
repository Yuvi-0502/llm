from pydantic import BaseModel


class UserCredentials(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_role: str
