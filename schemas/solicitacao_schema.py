from datetime import date

from pydantic import BaseModel, field_validator
from tortoise.fields import DateField

from models.solicitacao import ProdutosEnum

def validacao_nf(valor):
    if len(valor) != 15 or not valor.isdigit():
        raise ValueError("O número da NF deve conter exatamente 15 dígitos numéricos, sem espaços.")
    return valor

def validacao_num_serie(valor):
    if len(valor) != 10 or not valor.isdigit():
        raise ValueError("O número de serie de um produto deve conter exatamente 10 dígitos numéricos, sem espaços.")
    return valor

def validacao_produto(valor):
    try:
        return ProdutosEnum(valor)
    except ValueError:
        raise ValueError(
        f"O valor '{valor}' não é válido. Deve ser um dos seguintes: {[produto.value for produto in ProdutosEnum]}")

class SolicitacaoIn(BaseModel):
    num_nf: str
    produto: str
    num_serie: str
    descricao_defeito: str

    @field_validator("num_nf")
    def validar_num_nf(cls, value):
        return validacao_nf(value)

    @field_validator("produto")
    def validar_produto(cls, value):
        return validacao_produto(value)

    @field_validator("num_serie")
    def validar_num_serie(cls, value):
        return validacao_num_serie(value)

class SolicitacaoBaseOut(BaseModel):
    id: str
    status: str
    data_criacao: date
    num_nf: str
    produto: str
    descricao_defeito: str

