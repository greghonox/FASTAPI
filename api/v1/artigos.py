from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigos import Artigos
from models.usuarios import Usuarios
from schemas.artigos import Artigos as ArtigosSchemas

from core.deps import get_current_user, get_session

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArtigosSchemas)
async def post(artigo: ArtigosSchemas, usuario: Usuarios = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    novo_artigo: Artigos = Artigos(
        titulo=artigo.titulo, descricao=artigo.descricao, url=artigo.url, usuario_id=usuario.id)
    db.add(novo_artigo)
    await db.commit()
    return novo_artigo

@router.get('/', response_model=List[ArtigosSchemas])
async def get(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Artigos)
        result = await session.execute(query)
        artigos: List[Artigos] = result.scalars().unique().all()
        return artigos

@router.get('/{artigo_id}', response_model=ArtigosSchemas, status_code=status.HTTP_200_OK)
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(Artigos).filter(Artigos.id == artigo_id)
        result = await session.execute(query)
        artigo: Artigos = result.scalars().unique().one_or_none()
        if artigo:
            return artigo
        else:
            raise HTTPException(detail='Artigo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)

@router.put('/{artigo_id}', response_model=ArtigosSchemas, status_code=status.HTTP_202_ACCEPTED)
async def put_artigo(artigo_id: int, artigo: ArtigosSchemas, db: AsyncSession = Depends(get_session), usuario: Usuarios = Depends(get_current_user)):
    async with db as session:
        query = select(Artigos).filter(Artigos.id == artigo_id)
        result = await session.execute(query)
        artigo_up: Artigos = result.scalars().unique().one_or_none()

        if artigo_up:
            if artigo.titulo:
                artigo_up.titulo = artigo.titulo
            if artigo.descricao:
                artigo_up.descricao = artigo.descricao
            if artigo.url:
                artigo_up.url = artigo.url
            if usuario.id != artigo_up.usuario_id:
                artigo_up.usuario_id = usuario.id

            await session.commit()

            return artigo_up
        else:
            raise HTTPException(detail='Artigo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)

@router.delete('/{artigo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(artigo_id: int, db: AsyncSession = Depends(get_session), usuario: Usuarios = Depends(get_current_user)):
    async with db as session:
        query = select(Artigos).filter(Artigos.id == artigo_id)
        result = await session.execute(query)
        artigo_del: Artigos = result.scalars().unique().one_or_none()

        if artigo_del:
            await session.delete(artigo_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Artigo não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)