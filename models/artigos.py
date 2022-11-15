from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class Artigos(settings.DBBaseModel):
    __tablename__ = 'artigos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(256))
    descricao = Column(String(256))
    url = Column(String(256))
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    criador = relationship(
        "Usuarios", back_populates='artigos', lazy='joined')
