from fastapi import FastAPI, HTTPException, status, Path, Query, Header
from models import Cursos
from typing import Any
import uvicorn

app = FastAPI()

aulas = {
    1: {
        'titulo': 'Aula de programação',
        'aula': 111,
        'horas': 56
    },
    2: {
        'titulo': 'Aula de fastapi',
        'aula': 11,
        'horas': 51
    },    
}


@app.get('/')
async def raiz() -> dict:
    return {'msg': 'MSG INIT'}

@app.get('/mensagem')
async def message() -> str:
    return 'message fastapi'

@app.get('/cursos')
def get_cursos():
    return aulas

@app.get('/cursos/{curso_id}')
def get_cursos(curso_id:int=Path(default=None, title='ID do curso', 
                                 description='Deve ser entre 1, 10', gt=1, lt=11)) -> dict:
    try:
        return aulas[curso_id]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='curso não encontrado')

@app.post('/cursos')
def post_cursos(curso: Cursos) -> dict:
    if curso.id in aulas:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Curso já existe! {curso}')
    next_id = len(aulas) + 1 if curso.id is None else curso.id
    aulas[next_id] = curso
    aulas[next_id].id = next_id
    return aulas[next_id]
        
@app.put('/cursos/{curso_id}')
def put_cursos(curso_id: int, curso: Cursos) -> dict:
    if curso_id in aulas:
        aulas[curso_id] = curso
        return aulas[curso_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Curso id {curso_id} nao foi encontrado')

@app.delete('/cursos/{curso_id}')    
def delete_cursos(curso_id: int) -> dict:
    if curso_id in aulas:
        curso = aulas[curso_id]
        del aulas[curso_id]
        return curso
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Curso id {curso_id} nao foi encontrado')

@app.get('/calc')
def calc(a: int=Query(gt=0), b: int=Query(gt=0, default=1),
         c:str=Query(default='+', regex='[/|-|*]'),
         headerone: Any=Header(default=None), 
         headertwo: Any=Header(default=None)) -> dict:
    
    print(f'headers da pagina: \nheaderone:{headerone}\nheadertwo:{headertwo}')
    
    return {'a': a, 'b': b, 'c': eval(f'{a}{c}{b}')}


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', 
                port=8000, log_level='info', reload=True, debug=True)