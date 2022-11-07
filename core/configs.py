from pydantic import BaseSettings

class Settings(BaseSettings):
    """
         CONFIGURACAO DO APP
    """
    DB_URL: str = 'sqlite+aiosqlite:///database.db'
    API_VERSION: str = '/v1'

    class Config:
        case_sensitive = True
        
    def __str__(self) -> str:
        return f'URL: {self.URL_BASE} VERSION: {self.API_VERSION}'
    

settings: Settings = Settings()        