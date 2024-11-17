class EmailJaCadastradoException(Exception):
    def __init__(self):
        self.mensagem = "Email ja cadastrado"

class LoginInvalidoException(Exception):
    def __init__(self):
        self.mensagem = "Dados de login invalidos"

class MatriculaJaCadastradaException(Exception):
    def __init__(self):
        self.mensagem = "Matricula ja cadastrada"

class UsuarioNaoEncontradoException(Exception):
    def __init__(self):
        self.mensagem = "Usuario nao encontrado"

class AdminDesativacaoException(Exception):
    def __init__(self):
        self.mensagem = "Usuario admin não pode se desativar"

class UsuarioDesativadoException(Exception):
    def __init__(self):
        self.mensagem = "Não é possível atualizar um usuario desativado"
