from typing import Optional
from pydantic import BaseModel, validator


class Cursos(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: float
    horas: float
    
    def __str__(self) -> str:
        return f'{self.id} {self.titulo} {self.aulas} {self.horas}'
    
    @validator('titulo')
    def validator_titulo(cls, value) -> str:
        if len(value) >= 5:
            return value
        raise ValueError('O titulo deve ter mais caracteres!')
    
    @validator('aulas')
    def validator_aulas(cls, value) -> float:
        if value >= 14.9:
            return value
        raise ValueError('Deve ter aulas com mais 15 horas!')
    
    @validator('horas')
    def validator_horas(cls, value) -> float:
        if value >= 15:
            return value
        raise ValueError('Deve ter pelo menos 15 aulas!')


cursos = [
    Cursos(id=1, titulo='Aula de programação', aulas=15.1, horas=56),
    Cursos(id=2, titulo='Aula de fastapi', aulas=110, horas=51),
]