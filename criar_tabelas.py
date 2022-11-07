from asyncio import run
from sqlmodel import SQLModel
from core.database import engine
import models.cursos

async def create_tables() -> None:
    print('CRIANDO TABELAS NO BANCO')
    async with engine.begin() as conn:
        await conn.run_sync((SQLModel.metadata.drop_all))
        await conn.run_sync((SQLModel.metadata.create_all))
    print(f'CRIADO AS TABELAS COM SUCESSO!')
    
if __name__ == '__main__':
    run(create_tables())