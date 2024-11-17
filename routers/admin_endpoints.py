from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status

from core.security.security import get_current_user, validar_role
from exceptions.erro_interno_exception import ErroInternoException
from exceptions.usuario_exception import EmailJaCadastradoException, MatriculaJaCadastradaException, \
    UsuarioNaoEncontradoException, AdminDesativacaoException, UsuarioDesativadoException
from models.usuario import RoleEnum, Usuario
from schemas.usuario_schema import UsuarioIn, UsuarioOut, UsuarioUpdate
from services.admin_service import criar_usuario, buscar_usuario, desativar_usuario, atualizar_usuario

admin_router = APIRouter(prefix="/admin")

@admin_router.post("/create/user", status_code=status.HTTP_201_CREATED, response_model=UsuarioOut)
async def create_user(dados_usuario: UsuarioIn, usuario_corrente: Usuario = Depends(get_current_user)):
    validar_role(usuario_corrente, [RoleEnum.ADMIN])
    try:
        usuario = await criar_usuario(dados_usuario, usuario_corrente)
    except (EmailJaCadastradoException, MatriculaJaCadastradaException) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e.mensagem))
    except ErroInternoException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e.mensagem))

    return usuario

@admin_router.patch("/update/user")
async def update_user(dados_atualizados: UsuarioUpdate, usuario_corrente: Usuario = Depends(get_current_user)):
    validar_role(usuario_corrente, [RoleEnum.ADMIN])
    try:
        usuario_atualizado: UsuarioOut = await atualizar_usuario(dados_atualizados)
    except UsuarioNaoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.mensagem))
    except EmailJaCadastradoException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e.mensagem))
    except UsuarioDesativadoException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e.mensagem))
    except ErroInternoException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e.mensagem))

    return usuario_atualizado

@admin_router.patch("/deactivate/user/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_user(id_usuario: str, usuario_corrente: Usuario = Depends(get_current_user)):
    validar_role(usuario_corrente, [RoleEnum.ADMIN])
    try:
        await desativar_usuario(usuario_corrente, id_usuario)
    except UsuarioNaoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.mensagem))
    except AdminDesativacaoException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.mensagem))
    except ErroInternoException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e.mensagem))

@admin_router.get("/user/{id_usuario}", status_code=status.HTTP_200_OK, response_model=UsuarioOut)
async def get_user(id_usuario: str, usuario_corrente: Usuario = Depends(get_current_user)):
    validar_role(usuario_corrente, [RoleEnum.ADMIN])
    try:
        usuario = await buscar_usuario(id_usuario)
    except UsuarioNaoEncontradoException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.mensagem))
    except ErroInternoException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e.mensagem))

    return usuario