from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: str
    role: str

    def to_dict(self):
        return {
            'sub': self.sub,
            'role': self.role,
        }