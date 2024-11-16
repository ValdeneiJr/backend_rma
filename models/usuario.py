from tortoise.models import Model
from tortoise import fields
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = 'admin'
    SUP = "sup"
    FUNC = "func"

class Usuario(Model):
    id = fields.TextField(primary_key=True)
    matricula = fields.CharField(max_length=10, unique=True, null=False)
    nome = fields.TextField(null=False)
    email = fields.CharField(max_length=256, null=False, unique=True)
    role = fields.CharEnumField(RoleEnum, null=False)
    hash_senha = fields.TextField(null=False)
    status = fields.BooleanField(default=True)
    data_criacao = fields.DateField(auto_now_add=True)

    criador: fields.ForeignKeyNullableRelation["Usuario"] = (
        fields.ForeignKeyField("models.Usuario", related_name="usuarios_criados", null=True))
