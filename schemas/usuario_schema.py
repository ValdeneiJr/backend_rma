from pydantic import BaseModel, EmailStr, field_validator


def validar_nome(valor: str) -> str:
    if not all(part.isalpha() for part in valor.split()) or len(valor) < 6:
        raise ValueError("O campo 'nome' deve conter apenas letras e ter no mínimo 6 caracteres.")
    return valor

def validar_matricula(valor: str) -> str:
    if not valor.isdigit() or len(valor) != 10 or " " in valor:
        raise ValueError("A matrícula deve conter exatamente 10 dígitos, "
                         "apenas números, e não pode conter espaços em branco.")
    return valor

def validar_senha(valor: str) -> str:
    if len(valor) < 8 or not any(c.isalpha() for c in valor) or not any(c.isdigit() for c in valor) or " " in valor:
        raise ValueError("A senha deve ter pelo menos 8 caracteres, conter letras e números, "
                         "e não pode ter espaços em branco.")
    return valor

class UsuarioIn(BaseModel):
    matricula: str
    nome: str
    email: EmailStr
    role: str
    senha: str

    @field_validator("nome")
    def valida_nome(cls, valor) -> str:
        return validar_nome(valor)

    @field_validator("matricula")
    def valida_matricula(cls, valor: str) -> str:
        return validar_matricula(valor)

    @field_validator("senha")
    def valida_senha(cls, valor):
        return validar_senha(valor)

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

class UsuarioUpdate(BaseModel):
    id: str
    nome: str
    email: EmailStr
    role: str

    @field_validator("nome")
    def valida_nome(cls, valor) -> str:
        return validar_nome(valor)
