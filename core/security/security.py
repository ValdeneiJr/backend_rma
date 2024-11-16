from datetime import datetime, timedelta
from enum import Enum

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, DecodeError, ExpiredSignatureError, encode
from starlette import status

from core.config import SECRET_KEY, ALGORITHM, TEMPO_EXP
from models import Usuario
from schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

class RoleEnum(str, Enum):
    ADMIN = "admin"
    SUP = "sup"
    FUNC = "func"

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Não foi possivel validar as credenciais")

    try:
        payload = decode(token, SECRET_KEY, ALGORITHM)
        matricula: str = payload.get('sub')
        role: str = payload.get('role')

        if not matricula or not role:
            raise credentials_exception
    except DecodeError as e:
        print(e)
        raise credentials_exception
    except ExpiredSignatureError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")

    usuario = await Usuario.filter(matricula=matricula).first()

    if not usuario:
        raise credentials_exception

    if not usuario.status:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Acesso desativado")

    return usuario

def gerar_token(data: TokenData):
    exp = datetime.utcnow() + timedelta(hours=TEMPO_EXP)
    exp = int(exp.timestamp())

    data_token = data.to_dict()
    data_token['exp'] = exp

    encoded_token = encode(data_token, SECRET_KEY, ALGORITHM)

    return encoded_token

def validar_role(usuario, required_role):
    if not RoleEnum(usuario.role) == required_role.value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario sem permissao")
