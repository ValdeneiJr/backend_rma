import uuid
from datetime import date

from tortoise.exceptions import BaseORMException

from core.security.hashing import hashing_senha
from exceptions.usuario_exception import EmailJaCadastradoException, MatriculaJaCadastradaException, \
    UsuarioNaoEncontradoException, AdminDesativacaoException, UsuarioDesativadoException
from exceptions.erro_interno_exception import ErroInternoException
from mappers.usuario_mapper import usuario_model_usuario_out
from models.usuario import RoleEnum, Usuario
from schemas.usuario_schema import UsuarioIn, UsuarioOut, UsuarioUpdate


async def buscar_usuario(id_usuario):
    try:
        usuario = await Usuario.filter(id=id_usuario).first()
        if not usuario:
            raise UsuarioNaoEncontradoException()
    except BaseORMException:
        raise ErroInternoException()

    return usuario_model_usuario_out(usuario)

async def criar_usuario(dados_usuario: UsuarioIn, admin: Usuario):

    await matricula_cadastrada(dados_usuario.matricula)
    await email_cadastrado(dados_usuario.email)

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

    return usuario_model_usuario_out(usuario)

async def atualizar_usuario(novos_dados: UsuarioUpdate) -> UsuarioOut:
    try:
        usuario = await Usuario.filter(id=novos_dados.id).first()

        if not usuario:
            raise UsuarioNaoEncontradoException()
        if not usuario.status:
            raise UsuarioDesativadoException()

        valores_atualizados = False

        if novos_dados.nome != usuario.nome:
            setattr(usuario, 'nome', novos_dados.nome)
            valores_atualizados = True
        if novos_dados.role != usuario.role:
            setattr(usuario, 'role', RoleEnum(novos_dados.role))
            valores_atualizados = True
        if novos_dados.email != usuario.email:
            await email_cadastrado(novos_dados.email)
            setattr(usuario, 'email', novos_dados.email)
            valores_atualizados = True
        if valores_atualizados:
            await usuario.save()
    except BaseORMException as e:
        raise ErroInternoException()

    usuario_atualizado = usuario_model_usuario_out(usuario)
    return usuario_atualizado

async def desativar_usuario(admin, id_usuario):
    try:
        usuario = await Usuario.filter(id=id_usuario).first()
        if not usuario:
            raise UsuarioNaoEncontradoException()

        if usuario.id == admin.id:
            raise AdminDesativacaoException()

        usuario.status = False
        await usuario.save()
    except BaseORMException:
        raise ErroInternoException()

async def email_cadastrado(email):
    try:
        usuario = await Usuario.filter(email=email).first()
    except BaseORMException as e:
        raise ErroInternoException()
    if usuario:
        raise EmailJaCadastradoException()


async def matricula_cadastrada(matricula):
    try:
        usuario = await Usuario.filter(matricula=matricula).first()
    except BaseORMException as e:
        raise ErroInternoException()

    if usuario:
        raise MatriculaJaCadastradaException()