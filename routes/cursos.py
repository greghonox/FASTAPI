from fastapi import APIRouter, Depends, Header, Path, status, Response
from fastapi.exceptions import HTTPException
from core.deps import get_session
from typing import List, Any
from schemas.cursos import CursoSchema
from models.cursos import CursosModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


URL_BASE = '/cursos'
route = APIRouter()


@route.post(URL_BASE, status_code=status.HTTP_201_CREATED, response_model=CursoSchema)
async def post_cursos(curso: CursoSchema, db: AsyncSession=Depends(get_session)) -> dict:
    novo_curso = CursosModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)
    async with db as session:
        session.add(novo_curso)
        await session.commit()
    return curso


@route.get(URL_BASE, status_code=status.HTTP_201_CREATED,
                    description='Retornar todos os cursos que estão em memoria',
                    summary=f'Lista de cursos {CursoSchema}',
                    response_model=List[CursoSchema])
async def get_cursos(db: Any = Depends(get_session)):
    query = select(CursosModel)
    async with db as session:
        result = await session.execute(query)
        cursos: List[CursosModel] = result.scalars().all()
    return cursos

@route.get(URL_BASE + '/{curso_id}', status_code=status.HTTP_200_OK,
           response_model=CursoSchema)
async def get_cursos_id(curso_id:int=Path(default=None, title='ID do curso', 
              description='Deve ser entre 1, 10', gt=1, lt=11), 
              db: Any = Depends(get_session)) -> CursoSchema:
    query = select(CursosModel).filter(CursosModel.id == curso_id)
    async with db as session:
        result = await session.execute(query)
        curso: List[CursosModel] = result.scalars().one_or_none()
    
    if curso is None:
        HTTPException(detail='Curso não encontrado', status_code=status.HTTP_404_NOT_FOUND)
        
    return curso


@route.put(URL_BASE + '/{curso_id}')
async def put_cursos(curso_id: int, curso: CursoSchema, db: Any = Depends(get_session)) -> CursosModel:
    query = select(CursosModel).filter(CursosModel.id == curso_id)
    async with db as session:
        result = await db.execute(query)
        curso_up = result.scalar_one_or_none()
        if curso_up:
            curso_up.titulo = curso.titulo
            curso_up.aulas = curso.aulas
            curso_up.horas = curso.horas
            await session.commit()
            return curso_up
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Curso id {curso_id} nao foi encontrado')

@route.delete(URL_BASE + '/{curso_id}')    
async def delete_cursos(curso_id: int, db: Any = Depends(get_session)) -> dict:
    query = select(CursosModel).filter(CursosModel.id == curso_id)
    async with db as session:
        result = await db.execute(query)
        curso = result.scalar_one_or_none()
        if curso:
            await session.delete(curso)
            await session.commit()
            return curso

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Curso id {curso_id} nao foi encontrado')            