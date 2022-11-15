from secrets import token_urlsafe
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    """
         CONFIGURACAO DO APP
         PARA GERAR UM SECRET ALEATORIO PODE SE USAR O SEGUINTE SCRIPT:
         import secrets
         token: str = secrets.token_urlsafe(32)
    """
    DB_URL: str = 'sqlite+aiosqlite:///database.db'
    API_VERSION: str = '/v1'
    DBBaseModel = declarative_base()
    
    JWT_SECRET: str = '21Yu1GnmpQY9IGFfcCJB36wf1OIVUYZrqDKlwptWExE'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = 'HS256'
    
    

    class Config:
        case_sensitive = True # declara diferenca entre maiusculo e minusculo
        
    def __str__(self) -> str:
        return f'URL: {self.URL_BASE} VERSION: {self.API_VERSION}'
    

settings: Settings = Settings()        