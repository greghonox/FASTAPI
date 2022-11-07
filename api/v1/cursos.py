from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar
from sqlmodel import select

from models.cursos import Cursos
from core.deps import get_session

# Ignorar os warns
SelectOfScalar.inherit_cache = True # type: ignore
Select.inherit_cache = True # type: ignore

route: APIRouter = APIRouter()

URL_BASE = '/cursos'

@route.post(URL_BASE, status_code=status.HTTP_201_CREATED, response_model=Cursos, tags=['cursos'])
async def post_cursos(curso: Cursos, db: AsyncSession=Depends(get_session)) -> dict:
    novo_curso = Cursos(titulo=curso.titulo, horas=curso.horas, aulas=curso.aulas)
    db.add(novo_curso)
    await db.commit()
    return novo_curso


@route.get(URL_BASE, status_code=status.HTTP_200_OK, response_model=List[Cursos])
async def get_cursos(db: AsyncSession=Depends(get_session)) -> List[Cursos]:
    async with db as session:
        query = select(Cursos)
        result = await session.execute(query)
        cursos: List[Cursos] = result.scalars().all()
    return cursos


@route.get(URL_BASE+ '/{curso_id}', status_code=status.HTTP_200_OK, response_model=Cursos)
async def get_cursos_id(curso_id: int, db: AsyncSession=Depends(get_session)) -> Cursos:
    async with db as session:
        query = select(Cursos).filter(Cursos.id == curso_id)
        result = await session.execute(query)
        cursos: List[Cursos] = result.scalar_one_or_none()
        if cursos:
            return cursos    
        raise HTTPException(detail=f'Curso {curso_id} não encontrado', status_code=status.HTTP_404_NOT_FOUND)
    

@route.put(URL_BASE+ '/{curso_id}', status_code=status.HTTP_202_ACCEPTED, response_model=Cursos)
async def put_curso(curso_id: int, curso: Cursos, db: AsyncSession=Depends(get_session)) -> Cursos:
    async with db as session:
        query = select(Cursos).filter(Cursos.id == curso_id)
        result = await session.execute(query)
        cursos_up: List[Cursos] = result.scalar_one_or_none()
        if cursos_up:
            cursos_up.titulo = curso.titulo
            cursos_up.aulas = curso.aulas
            cursos_up.horas = curso.horas
            
            await session.commit()
            return cursos_up    
        raise HTTPException(detail=f'Curso {curso_id} não encontrado', status_code=status.HTTP_404_NOT_FOUND)    
    

@route.delete(URL_BASE+ '/{curso_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession=Depends(get_session)) -> Response:
    async with db as session:
        query = select(Cursos).filter(Cursos.id == curso_id)
        result = await session.execute(query)
        curso: List[Cursos] = result.scalar_one_or_none()
        if curso:
            await session.delete(curso)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)    
        raise HTTPException(detail=f'Curso {curso_id} não encontrado', status_code=status.HTTP_404_NOT_FOUND)        