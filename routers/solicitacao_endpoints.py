from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status

from core.security.security import get_current_user, RoleEnum, validar_role
from exceptions.erro_interno_exception import ErroInternoException
from exceptions.solicitacao_exception import SolicitacaoJaCadastradaException, SolicitacaoNaoEncontradaException, \
    SolicitacaoStatusException, SolicitacaoAnaliseException, SolicitacaoJaConcluidaException, \
    SolicitacaoNaoPodeSerFechadaException
from models import Usuario
from schemas.solicitacao_schema import SolicitacaoIn, SolicitacaoBaseOut, SolicitacaoUpdate, SolicitacaoOut, \
    SolicitacaoAnalise
from services.solicitacao_service import criar_solicitacao, atualizar_solicitacao, adicionar_analise, \
    concluir_solicitacao, buscar_solicitacao

solicitacao_router = APIRouter(prefix='/request')

@solicitacao_router.post('/create', status_code=status.HTTP_201_CREATED, response_model=SolicitacaoBaseOut)
async def create_request(dados_sol: SolicitacaoIn, usuario_corrente: Usuario = Depends(get_current_user)):
    validar_role(usuario_corrente, [RoleEnum.FUNC])
    try:
        solicitacao = await criar_solicitacao(dados_sol, usuario_corrente)
    except SolicitacaoJaCadastradaException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e.mensagem))
    except ErroInternoException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e.mensagem))

    return solicitacao

@solicitacao_router.patch("/update", status_code=status.HTTP_200_OK, response_model=SolicitacaoBaseOut)
async def update_request(novos_dados: SolicitacaoUpdate, usuario_corrente: Usuario = Depends(get_current_user)):
    validar_role(usuario_corrente, [RoleEnum.FUNC])
    try:
        solicitacao = await atualizar_solicitacao(novos_dados, usuario_corrente)
    except SolicitacaoNaoEncontradaException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.mensagem))
    except SolicitacaoStatusException as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e.mensagem))
    except ErroInternoException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e.mensagem))

    return solicitacao

@solicitacao_router.patch("/analysis", status_code=status.HTTP_200_OK, response_model=SolicitacaoOut)
async def insert_analysis(dados_analise: SolicitacaoAnalise, usuario_corrente: Usuario = Depends(get_current_user)):
    validar_role(usuario_corrente, [RoleEnum.FUNC])
    try:
        solicitacao = await adicionar_analise(dados_analise, usuario_corrente)
    except SolicitacaoNaoEncontradaException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.mensagem))
    except SolicitacaoAnaliseException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e.mensagem))
    except ErroInternoException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e.mensagem))

    return solicitacao

@solicitacao_router.patch("/finalize/{id_sol}", status_code=status.HTTP_200_OK, response_model=SolicitacaoOut)
async def close_request(id_sol: str, usuario_corrente: Usuario = Depends(get_current_user)):
    validar_role(usuario_corrente, [RoleEnum.FUNC])
    try:
        solicitacao = await concluir_solicitacao(id_sol, usuario_corrente)
    except SolicitacaoNaoEncontradaException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.mensagem))
    except SolicitacaoJaConcluidaException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e.mensagem))
    except SolicitacaoNaoPodeSerFechadaException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e.mensagem))
    except ErroInternoException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e.mensagem))

    return solicitacao

@solicitacao_router.get("/{id_sol}", status_code=status.HTTP_200_OK, response_model=SolicitacaoOut)
async def get_request(id_sol: str, usuario_corrente: Usuario = Depends(get_current_user)):
    validar_role(usuario_corrente, [RoleEnum.FUNC, RoleEnum.SUP])
    try:
        solicitacao = await buscar_solicitacao(id_sol)
    except SolicitacaoNaoEncontradaException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.mensagem))
    except ErroInternoException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e.mensagem))

    return solicitacao