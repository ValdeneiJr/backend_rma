class SolicitacaoJaCadastradaException(Exception):
    def __init__(self):
        self.mensagem = "Já existe uma solicitação em aberto para este produto"

class SolicitacaoNaoEncontradaException(Exception):
    def __init__(self):
        self.mensagem = "Solicitação não encontrada"

class SolicitacaoStatusException(Exception):
    def __init__(self):
        self.mensagem = "Neste estagio o status da solicitação pode ser atualizado apenas para 'em_analise'"

