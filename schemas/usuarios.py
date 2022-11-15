from typing import Optional, List
from pydantic import BaseModel, EmailStr

from schemas.artigos import Artigos


class Usuarios(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    admin: bool = False
    
    class Config:
        orm_mode = True
        
        
class UsuarioSchema(Usuarios):
    senha: str
    

class UsuarioSchemaArtigos(Usuarios):
    artigos: Optional[List[Artigos]]
    

class UsuarioSchemaUpdate(Usuarios):
    nome: Optional[str]
    sobrenome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    admin: Optional[bool]
    
