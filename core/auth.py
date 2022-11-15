from pytz import timezone

from typing import Optional, List
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.usuarios import Usuarios
from core.configs import settings
from core.security import verificar_senha
from pydantic import EmailStr

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_VERSION}/usuarios/login"
)

async def autenticar(email: EmailStr, senha:str, db: AsyncSession) -> Optional[Usuarios]:
    async with db as session:
        query = select(Usuarios).filter(Usuarios.email == email)
        result = await session.execute(query)
        usuario: Usuarios = result.scalars().unique().one_or_none()
        
        if not verificar_senha(email, usuario.senha):
            return usuario
        raise HTTPException(status_code=404)
    

def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    payload = {}
    local = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=local) + timedelta(tempo_vida)
    
    payload['type'] = tipo_token
    payload['exp'] = expira
    payload['iat'] = datetime.now(tz=local)
    payload['sub'] = str(sub)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def criar_token_acesso(sub: str) -> str:
    return _criar_token(
        tipo_token='token_acesso', 
        tempo_vida=settings.ACCESS_TOKEN_EXPIRE_MINUTES, 
        sub=sub)
