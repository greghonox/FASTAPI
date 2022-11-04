from typing import List
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    """
         CONFIGURACAO DO APP
    """
    DBBAseModel = declarative_base()
    API_VERSION: str = '1.00'
    DB_URL: str = 'sqlite+aiosqlite:///database.db'
    
    class Config:
        case_sensitive = True
        
    def __str__(self) -> str:
        return f'DB: {self.DBBAseModel} URL: {self.DB_URL} VERSION: {self.API_VERSION}'
    
    
settings = Settings()