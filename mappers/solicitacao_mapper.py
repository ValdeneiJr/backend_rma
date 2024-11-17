from models import Solicitacao
from schemas.solicitacao_schema import SolicitacaoBaseOut

def sol_model_to_base_out(solicitacao: Solicitacao) -> SolicitacaoBaseOut:
    return SolicitacaoBaseOut(
        id=solicitacao.id,
        status=solicitacao.status,
        data_criacao=solicitacao.data_criacao,
        num_nf=solicitacao.num_nf,
        produto=solicitacao.produto,
        descricao_defeito=solicitacao.descricao_defeito
    )