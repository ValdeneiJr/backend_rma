from pydantic import BaseModel
from typing_extensions import Optional


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    matricula: Optional[str] = None
    role: Optional[str] = None

    def to_dict(self):
        return {
            'matricula': self.matricula,
            'role': self.role,
        }