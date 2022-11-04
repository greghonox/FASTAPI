from typing import Optional
from pydantic import BaseModel as Base

class CursoSchema(Base):
    id: Optional[int]
    titulo: str
    horas: int
    aulas: int
    
    class Config:
        orm_mode = True