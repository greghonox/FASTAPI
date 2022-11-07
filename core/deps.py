from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Session

async def get_session() -> Generator:
    session: AsyncSession = Session()
    try:
        yield session
        
    except Exception as e:
        print(f'Erro encontrado ao manipular banco: {e}')
        await session.close()
        
    finally:
        await session.close()