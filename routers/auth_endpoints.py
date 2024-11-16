from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from exceptions.erro_interno_exception import ErroInternoException
from exceptions.usuario_exception import LoginInvalidoException
from schemas.token import Token
from schemas.usuario import UsuarioLogin
from services.auth_service import login_usuario

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_para_token(form_dados_login: OAuth2PasswordRequestForm = Depends()):
    dados_login = UsuarioLogin(matricula=form_dados_login.username, senha=form_dados_login.password)
    try:
        token = await login_usuario(dados_login)
    except LoginInvalidoException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e.mensagem))
    except ErroInternoException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e.mensagem))

    return token