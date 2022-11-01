from typing import Optional
from pydantic import BaseModel

class Cursos(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: str
    horas: float
    
    def __str__(self) -> str:
        return f'{self.id} {self.titulo} {self.aulas} {self.horas}'