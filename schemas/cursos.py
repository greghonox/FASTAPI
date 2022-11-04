from typing import Optional
from pydantic import BaseModel as Base

class CursosSchema(Base):
    id: Optional[int]
    titulo: str
    horas: int
    aulas: int
    
    class Config:
        orm_mode = True