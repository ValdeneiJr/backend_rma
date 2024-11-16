from tortoise.exceptions import BaseORMException

from core.security.hashing import verificar_senha
from core.security.security import gerar_token
from exceptions.erro_interno_exception import ErroInternoException
from exceptions.usuario_exception import LoginInvalidoException
from models import Usuario
from schemas.token import TokenData, Token
from schemas.usuario import UsuarioLogin

async def login_usuario(dados_login: UsuarioLogin):
    try:
        usuario = await Usuario.filter(matricula=dados_login.matricula).first()
    except BaseORMException as e:
        raise ErroInternoException()

    if not usuario:
        raise LoginInvalidoException()

    if not verificar_senha(dados_login.senha, usuario.hash_senha):
        raise LoginInvalidoException()

    encoded_token = gerar_token(TokenData(matricula=usuario.matricula, role=usuario.role))

    return Token(access_token=encoded_token, token_type="Bearer")