from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status

from core.security.security import get_current_user, validar_role
from exceptions.erro_interno_exception import ErroInternoException
from exceptions.usuario_exception import EmailJaCadastradoException, MatriculaJaCadastradaException
from models.usuario import RoleEnum, Usuario
from schemas.usuario import UsuarioIn
from services.admin_service import criar_usuario

admin_router = APIRouter(prefix="/admin")

@admin_router.post("/create/user")
async def create_user(body: UsuarioIn, usuario_corrente: Usuario = Depends(get_current_user)):
    validar_role(usuario_corrente, RoleEnum.ADMIN)
    try:
        usuario = await criar_usuario(body, usuario_corrente)
    except (EmailJaCadastradoException, MatriculaJaCadastradaException) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e.mensagem))
    except ErroInternoException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e.mensagem))

    return usuario
