from models import Solicitacao
from schemas.solicitacao_schema import SolicitacaoBaseOut, SolicitacaoOut


def sol_model_to_base_out(solicitacao: Solicitacao) -> SolicitacaoBaseOut:
    return SolicitacaoBaseOut(
        id=solicitacao.id,
        status=solicitacao.status,
        data_criacao=solicitacao.data_criacao,
        num_nf=solicitacao.num_nf,
        produto=solicitacao.produto,
        num_serie_produto= solicitacao.num_serie_produto,
        descricao_defeito=solicitacao.descricao_defeito
    )

def sol_model_to_out(solicitacao: Solicitacao) -> SolicitacaoOut:
    return SolicitacaoOut(
        id=solicitacao.id,
        status=solicitacao.status,
        data_criacao=solicitacao.data_criacao,
        num_nf=solicitacao.num_nf,
        produto=solicitacao.produto,
        num_serie_produto= solicitacao.num_serie_produto,
        descricao_defeito=solicitacao.descricao_defeito,
        descricao_analise=solicitacao.descricao_analise,
        resultado_analise=solicitacao.resultado_analise
    )