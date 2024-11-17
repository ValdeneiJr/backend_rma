class SolicitacaoJaCadastradaException(Exception):
    def __init__(self):
        self.mensagem = "Já existe uma solicitação em aberto para este produto"