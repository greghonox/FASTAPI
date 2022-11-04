from core.configs import settings
from core.database import engine
from models import __all_models
from asyncio import run


async def create_tables() -> None:
    print('criando as tabela no banco de dados')
    
    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBAseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBAseModel.metadata.create_all)
    print('Tabelas criadas com sucesso!')
    

if __name__ == '__main__':
    run(create_tables())