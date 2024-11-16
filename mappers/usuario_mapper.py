from models.usuario import Usuario
from schemas.usuario_schema import UsuarioOut

def usuario_model_usuario_out(usuario: Usuario) -> UsuarioOut:
    return UsuarioOut(
        id=usuario.id,
        matricula=usuario.matricula,
        nome=usuario.nome,
        email=usuario.email,
        role=usuario.role,
        status=usuario.status
    )