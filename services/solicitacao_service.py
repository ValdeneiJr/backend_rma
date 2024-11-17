import uuid
from datetime import date

from tortoise.exceptions import BaseORMException

from exceptions.erro_interno_exception import ErroInternoException
from exceptions.solicitacao_exception import SolicitacaoJaCadastradaException
from mappers.solicitacao_mapper import sol_model_to_base_out
from models import Usuario
from models.solicitacao import Solicitacao, ProdutosEnum, StatusEnum
from schemas.solicitacao_schema import SolicitacaoIn, SolicitacaoBaseOut

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

async def verificar_sol_existente(num_nf: str, produto: ProdutosEnum, num_serie: str):
    try:
        sol = await Solicitacao.filter(num_nf=num_nf, produto=produto, num_serie_produto=num_serie).first()
    except BaseORMException as e:
        raise ErroInternoException()

    if sol:
        raise SolicitacaoJaCadastradaException()