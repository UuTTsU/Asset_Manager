from pydantic import BaseModel

#Token response model
class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class AccessTokenResponseSchema(BaseModel):
    access_token: str
    access_token: str = "bearer"

class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str