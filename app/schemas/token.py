from pydantic import BaseModel

#Token response model
class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str