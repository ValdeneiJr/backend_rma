import uuid

from tortoise.exceptions import BaseORMException

from core.security.hashing import hashing_senha
from exceptions.usuario_exception import EmailJaCadastradoException, MatriculaJaCadastradaException
from exceptions.erro_interno_exception import ErroInternoException
from models.usuario import RoleEnum, Usuario
from schemas.usuario import UsuarioIn, UsuarioOut


async def criar_usuario(dados_usuario: UsuarioIn):

    if await email_cadastrado(dados_usuario.email):
        raise EmailJaCadastradoException()

    if await matricula_cadastrada(dados_usuario.matricula):
        raise MatriculaJaCadastradaException()

    id_ = str(uuid.uuid4())
    role = RoleEnum(dados_usuario.role)
    hash_senha = hashing_senha(dados_usuario.senha)

    usuario = Usuario(
        id= id_,
        matricula= dados_usuario.matricula,
        nome=dados_usuario.nome,
        email=dados_usuario.email,
        role=role,
        hash_senha=hash_senha
    )

    try:
        await usuario.save()
    except BaseORMException as e:
        print(e)
        raise ErroInternoException()

    return UsuarioOut(
        matricula= dados_usuario.matricula,
        nome=dados_usuario.nome,
        email=dados_usuario.email,
        role=role,
    )

async def email_cadastrado(email):
    try:
        usuario = await Usuario.filter(email=email).first()
    except BaseORMException as e:
        raise ErroInternoException()

    if usuario:
        return True

    return False


async def matricula_cadastrada(matricula):
    try:
        usuario = await Usuario.filter(matricula=matricula).first()
    except BaseORMException as e:
        raise ErroInternoException()

    if usuario:
        return True

    return False