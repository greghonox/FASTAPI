from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from core.configs import settings

class Usuarios(settings.DBBaseModel):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(256), nullable=True)
    sobrenome = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=False, unique=True)
    senha = Column(String(256), nullable=False)
    admin = Column(Boolean, default=False)
    artigos = relationship(
        "Artigos",
        cascade="all,delete-orphan",
        back_populates="criador",
        uselist=True,
        lazy="joined"
    )