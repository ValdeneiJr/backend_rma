from fastapi import APIRouter, HTTPException
from starlette import status

from exceptions.erro_interno_exception import ErroInternoException
from exceptions.usuario_exception import EmailJaCadastradoException, MatriculaJaCadastradaException
from schemas.usuario import UsuarioIn
from services.admin_service import criar_usuario

admin_router = APIRouter(prefix="/admin")

@admin_router.post("/create/user")
async def create_user(body: UsuarioIn):
    try:
        usuario = await criar_usuario(body)
    except (EmailJaCadastradoException, MatriculaJaCadastradaException) as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e.message))
    except ErroInternoException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e.mensagem))

    return usuario
