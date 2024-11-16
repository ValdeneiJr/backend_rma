import uuid
from datetime import date

from tortoise.exceptions import BaseORMException

from core.security.hashing import hashing_senha
from exceptions.usuario_exception import EmailJaCadastradoException, MatriculaJaCadastradaException, \
    UsuarioNaoEncontradoException
from exceptions.erro_interno_exception import ErroInternoException
from models.usuario import RoleEnum, Usuario
from schemas.usuario import UsuarioIn, UsuarioOut

async def buscar_usuario(id_usuario):
    try:
        usuario = await Usuario.filter(id=id_usuario).first()
        if not usuario:
            raise UsuarioNaoEncontradoException()
    except BaseORMException:
        raise ErroInternoException()

    return UsuarioOut(
        id= usuario.id,
        matricula= usuario.matricula,
        nome=usuario.nome,
        email=usuario.email,
        role=usuario.role,
        status= usuario.status
    )

async def criar_usuario(dados_usuario: UsuarioIn, admin: Usuario):

    if await email_cadastrado(dados_usuario.email):
        raise EmailJaCadastradoException()

    if await matricula_cadastrada(dados_usuario.matricula):
        raise MatriculaJaCadastradaException()

    id_ = str(uuid.uuid4())
    role = RoleEnum(dados_usuario.role)
    hash_senha = hashing_senha(dados_usuario.senha)
    data = date.today()

    usuario = Usuario(
        id= id_,
        matricula= dados_usuario.matricula,
        nome=dados_usuario.nome,
        email=dados_usuario.email,
        role=role,
        hash_senha=hash_senha,
        data_criacao=data,
        criador = admin
    )

    try:
        await usuario.save()
    except BaseORMException as e:
        print(e)
        raise ErroInternoException()

    return UsuarioOut(
        id= usuario.id,
        matricula= usuario.matricula,
        nome=usuario.nome,
        email=usuario.email,
        role=usuario.role,
        status= usuario.status
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