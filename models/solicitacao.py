from enum import Enum

from tortoise.models import Model
from tortoise import fields

from models.usuario import Usuario


class StatusEnum(str, Enum):
    RECEBIDA = "recebida"
    EM_ANALISE = "em_analise"
    PROCESSAMENTO_TROCA = "processamento_troca"
    PROCESSAMENTO_REEMBOLSO = "processamento_reembolso"
    EM_REPARO = "em_reparo"
    CONCLUIDA = "concluida"

class ProdutosEnum(str, Enum):
    GELADEIRA = "geladeira"
    MICROONDAS = "microondas"
    MAQUINA_DE_LAVAR = "maquina_de_lavar"
    AR_CONDICIONADO = "ar_condicionado"
    ASPIRADOR_DE_PO = "aspirador_de_po"

class ResultAnaliseEnum(str, Enum):
    TROCA = "troca"
    REPARO = "reparo"
    REEMBOLSO = "reembolso"

class Solicitacao(Model):
    id = fields.TextField(primary_key=True)
    status = fields.CharEnumField(StatusEnum, default=StatusEnum.RECEBIDA, null=False)
    data_criacao = fields.DateField(null=False)
    num_nf = fields.TextField(null=False)
    produto = fields.CharEnumField(ProdutosEnum, null=False)
    descricao_defeito = fields.TextField(null=False)
    descricao_analise = fields.TextField(null=True)
    resultado_analise = fields.CharEnumField(ResultAnaliseEnum, null=True)
    data_fechamento = fields.DateField(null=True)

    resp_criacao: fields.ForeignKeyNullableRelation["Usuario"] = (
        fields.ForeignKeyField("models.Usuario", related_name="solicitacoes_criadas", null=False)
    )

    resp_analise: fields.ForeignKeyNullableRelation["Usuario"] = (
        fields.ForeignKeyField("models.Usuario", related_name="solicitacoes_analisadas", null=True)
    )
