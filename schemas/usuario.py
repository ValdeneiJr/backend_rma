from pydantic import BaseModel

class UsuarioIn(BaseModel):
    matricula: str
    nome: str
    email: str
    role: str
    senha: str

class UsuarioOut(BaseModel):
    matricula: str
    nome: str
    email: str
    role: str

class UsuarioLogin(BaseModel):
    matricula: str
    senha: str
