class ErroInternoException(Exception):
    def __init__(self):
        self.mensagem = "Erro interno"