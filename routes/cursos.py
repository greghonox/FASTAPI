from fastapi import APIRouter, Depends, Header, Path, status
from fastapi.exceptions import HTTPException
from models.cursos import Cursos, cursos
from modules.utils import choices
from typing import List, Any


URL_BASE = '/cursos'
route = APIRouter()


@route.get(URL_BASE, description='Retornar todos os cursos que estão em memoria',
                    summary=f'Lista de cursos {cursos}',
                    response_model=List[Cursos])
def get_cursos(request: Any = Depends(choices)):
    return cursos


@route.get(URL_BASE + '/{curso_id}', response_model=Cursos)
def get_cursos_id(curso_id:int=Path(default=None, title='ID do curso', 
              description='Deve ser entre 1, 10', 
              gt=1, lt=11), request: Any = Depends(choices)) -> dict:
    try:
        return cursos[curso_id - 1]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='curso não encontrado')


@route.post(URL_BASE)
def post_cursos(curso: Cursos) -> dict:
    if curso.id in cursos:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Curso já existe! {curso}')
    next_id = len(cursos) + 1 if curso.id is None else curso.id
    cursos[next_id] = curso
    cursos[next_id].id = next_id
    return cursos[next_id]


@route.put(URL_BASE + '/{curso_id}')
def put_cursos(curso_id: int, curso: Cursos, request: Any = Depends(choices)) -> dict:
    if curso_id in cursos:
        cursos[curso_id] = curso
        return cursos[curso_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Curso id {curso_id} nao foi encontrado')


@route.delete(URL_BASE + '/{curso_id}')    
def delete_cursos(curso_id: int, request: Any = Depends(choices)) -> dict:
    if curso_id in cursos:
        curso = cursos[curso_id]
        del cursos[curso_id]
        return curso
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Curso id {curso_id} nao foi encontrado')