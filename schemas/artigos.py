from typing import Optional
from pydantic import BaseModel, HttpUrl


class Artigos(BaseModel):
    id: Optional[int]
    titulo: str
    descricao: str
    url: Optional[HttpUrl]
    usuario_id: Optional[int]
    
    class Config:
        orm_mode = True