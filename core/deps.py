from pydantic import BaseModel
from jose import jwt, JWTError
from sqlalchemy.future import select
from typing import Generator, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from core.database import Session
from core.auth import oauth2_schema
from core.configs import settings
from models.usuarios import Usuarios

class TokenData(BaseModel):
    username: Optional[str] = None
    

async def get_session() -> Generator:
    session: AsyncSession = Session()
    try:
        yield session
        
    except Exception as e:
        print(f'Erro encontrado ao manipular banco: {e}')
        await session.close()
        
    finally:
        await session.close()
        

async def get_current_user(db: Session= Depends(get_session), 
                           token: str = Depends(oauth2_schema)) -> Usuarios:
    credential_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                        detail='Não foi possivel se autenticar a credencial',
                                        headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            [settings.ALGORITHM],
            options={'verify_aud': False}
        )
        username: str = payload.get('sub')
        if username is not None:
            token_data = TokenData(username=username)
            async with db as session:
                query = select(Usuarios).filter(Usuarios.id == int(token_data.username))
                result = await session.execute(query)
                usuario: Usuarios = result.scalars().unique().one_or_none()
                if usuario:
                    return usuario

        raise credential_exception
    except JWTError:
        raise credential_exception