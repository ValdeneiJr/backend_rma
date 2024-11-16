from pydantic import BaseModel

class UsuarioIn(BaseModel):
    matricula: str
    nome: str
    email: str
    role: str
    senha: str

class UsuarioOut(BaseModel):
    id: str
    matricula: str
    nome: str
    email: str
    role: str
    status: bool

class UsuarioLogin(BaseModel):
    matricula: str
    senha: str
