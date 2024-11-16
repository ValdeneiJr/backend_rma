class EmailJaCadastradoException(Exception):
    def __init__(self):
        self.message = "Email ja cadastrado"

class LoginInvalidoException(Exception):
    def __init__(self):
        self.mensagem = "Dados de login invalidos"

class MatriculaJaCadastradaException(Exception):
    def __init__(self):
        self.mensagem = "Matricula ja cadastrada"