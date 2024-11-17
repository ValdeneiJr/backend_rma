from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator

from models.solicitacao import ProdutosEnum, StatusEnum, ResultAnaliseEnum


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

def validacao_status(valor):
    try:
        return StatusEnum(valor)
    except ValueError:
        raise ValueError(
        f"O valor '{valor}' não é válido. Deve ser um dos seguintes: {[status.value for status in StatusEnum]}")

def validacao_resultado_analise(valor):
    try:
        return ResultAnaliseEnum(valor)
    except ValueError:
        raise ValueError(
        f"O valor '{valor}' não é válido. Deve ser um dos seguintes: {[resultado.value for resultado in ResultAnaliseEnum]}")

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
    num_serie_produto: str
    descricao_defeito: str

class SolicitacaoUpdate(BaseModel):
    id: str
    num_nf: str
    produto: str
    num_serie: str
    descricao_defeito: str
    status: str

    @field_validator("num_nf")
    def validar_num_nf(cls, value):
        return validacao_nf(value)

    @field_validator("produto")
    def validar_produto(cls, value):
        return validacao_produto(value)

    @field_validator("num_serie")
    def validar_num_serie(cls, value):
        return validacao_num_serie(value)

    @field_validator("status")
    def validar_status(cls, value):
        return validacao_status(value)

class SolicitacaoAnalise(BaseModel):
    id: str
    descricao_analise: str
    resultado_analise: str

    @field_validator("resultado_analise")
    def validar_resultado_analise(cls, value):
        return validacao_resultado_analise(value)

class SolicitacaoOut(BaseModel):
    id: str
    status: str
    data_criacao: date
    num_nf: str
    produto: str
    num_serie_produto: str
    descricao_defeito: str
    descricao_analise: str
    resultado_analise: str