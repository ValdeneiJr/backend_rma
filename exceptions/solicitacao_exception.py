class SolicitacaoJaCadastradaException(Exception):
    def __init__(self):
        self.mensagem = "Já existe uma solicitação em aberto para este produto"

class SolicitacaoNaoEncontradaException(Exception):
    def __init__(self):
        self.mensagem = "Solicitação não encontrada"

class SolicitacaoStatusException(Exception):
    def __init__(self):
        self.mensagem = "Neste estagio o status da solicitação pode ser atualizado apenas para 'em_analise'"

class SolicitacaoAnaliseException(Exception):
    def __init__(self):
        self.mensagem = "Apenas o funcionario responsavel pela analise pode preencher estes dados"

class SolicitacaoJaConcluidaException(Exception):
    def __init__(self):
        self.mensagem = "Essa solicitação ja foi concluida"

class SolicitacaoNaoPodeSerFechadaException(Exception):
    def __init__(self):
        self.mensagem = "Essa solicitação não pode ser concluida ainda, pois não foi analisada"