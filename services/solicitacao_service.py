import uuid
from datetime import date
from typing import Optional

from tortoise.exceptions import BaseORMException

from exceptions.erro_interno_exception import ErroInternoException
from exceptions.solicitacao_exception import SolicitacaoJaCadastradaException, SolicitacaoNaoEncontradaException, \
    SolicitacaoStatusException
from mappers.solicitacao_mapper import sol_model_to_base_out
from models import Usuario
from models.solicitacao import Solicitacao, ProdutosEnum, StatusEnum
from schemas.solicitacao_schema import SolicitacaoIn, SolicitacaoBaseOut, SolicitacaoUpdate


async def criar_solicitacao(dados_sol: SolicitacaoIn, usuario: Usuario) -> SolicitacaoBaseOut:
    await verificar_sol_existente(dados_sol.num_nf, ProdutosEnum(dados_sol.produto), dados_sol.num_serie)

    id_ = str(uuid.uuid4())
    data = date.today()
    produto = ProdutosEnum(dados_sol.produto)
    status = StatusEnum('recebida')

    solicitacao = Solicitacao(
        id=id_,
        status=status,
        data_criacao=data,
        num_nf = dados_sol.num_nf,
        produto=produto,
        num_serie_produto=dados_sol.num_serie,
        descricao_defeito=dados_sol.descricao_defeito,
        resp_criacao=usuario,
    )

    try:
        await solicitacao.save()
    except BaseORMException as e:
        print(e)
        raise ErroInternoException()

    return sol_model_to_base_out(solicitacao)

async def atualizar_solicitacao(novos_dados: SolicitacaoUpdate, usuario: Usuario):
    try:
        solicitacao = await Solicitacao.filter(id=novos_dados.id).first()

        if not solicitacao:
            raise SolicitacaoNaoEncontradaException()

        valores_atualizados = False

        if novos_dados.num_nf != solicitacao.num_nf:
            setattr(solicitacao, 'num_nf', novos_dados.num_nf)
            valores_atualizados = True
        if novos_dados.produto != solicitacao.produto:
            setattr(solicitacao, 'produto', ProdutosEnum(novos_dados.produto))
            valores_atualizados = True
        if novos_dados.num_serie != solicitacao.num_serie_produto:
            setattr(solicitacao, 'num_serie_produto', novos_dados.num_serie)
            valores_atualizados = True
        if novos_dados.descricao_defeito != solicitacao.descricao_defeito:
            setattr(solicitacao, 'descricao_defeito', novos_dados.descricao_defeito)
        if novos_dados.status != solicitacao.status:
            if novos_dados.status != 'em_analise':
                raise SolicitacaoStatusException()
            setattr(solicitacao, 'status', StatusEnum(novos_dados.status))
            setattr(solicitacao, 'resp_analise_id', usuario.id)
            valores_atualizados = True

        if valores_atualizados:
            await solicitacao.save()
            print("salvo")
    except BaseORMException as e:
        raise ErroInternoException()

    solicitacao_atualizada = sol_model_to_base_out(solicitacao)

    return solicitacao_atualizada

async def verificar_sol_existente(num_nf: str, produto: ProdutosEnum, num_serie: str):
    try:
        sol = await Solicitacao.filter(num_nf=num_nf, produto=produto, num_serie_produto=num_serie).first()
    except BaseORMException as e:
        raise ErroInternoException()

    if sol:
        raise SolicitacaoJaCadastradaException()