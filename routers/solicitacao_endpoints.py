from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status

from core.security.security import get_current_user, RoleEnum, validar_role
from exceptions.erro_interno_exception import ErroInternoException
from exceptions.solicitacao_exception import SolicitacaoJaCadastradaException
from models import Usuario
from schemas.solicitacao_schema import SolicitacaoIn, SolicitacaoBaseOut
from services.solicitacao_service import criar_solicitacao

solicitacao_router = APIRouter(prefix='/request')

@solicitacao_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=SolicitacaoBaseOut)
async def create_request(dados_sol: SolicitacaoIn, usuario_corrente: Usuario = Depends(get_current_user)):
    validar_role(usuario_corrente, RoleEnum.FUNC)
    try:
        solicitacao = await criar_solicitacao(dados_sol, usuario_corrente)
    except SolicitacaoJaCadastradaException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e.mensagem))
    except ErroInternoException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e.mensagem))

    return solicitacao