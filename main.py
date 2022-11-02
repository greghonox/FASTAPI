from fastapi import FastAPI, HTTPException, status, Path, Query, Header, Depends
from models import Cursos, cursos
from typing import Any, List
import uvicorn

from scripts.utils import choices

app = FastAPI(
    title='Aprendendo fastApi',
    version='0.0.1',
    description='Aprendendo fastApi para ficar bom'
    )



@app.get('/', description='APenas para saber que funciona',
              summary='Raiz de tudo')
async def raiz() -> dict:
    return {'msg': 'MSG INIT'}

@app.get('/mensagem', description='Para saber que funciona',
                      summary='Um breve teste!')
async def message() -> str:
    return 'message fastapi'

@app.get('/cursos', description='Retornar todos os cursos que estão em memoria',
                    summary=f'Lista de cursos {cursos}',
                    response_model=List[Cursos])
def get_cursos(request: Any = Depends(choices)):
    return cursos

@app.get('/cursos/{curso_id}', response_model=Cursos)
def get_cursos_id(curso_id:int=Path(default=None, title='ID do curso', 
              description='Deve ser entre 1, 10', 
              gt=1, lt=11), request: Any = Depends(choices)) -> dict:
    try:
        return cursos[curso_id - 1]
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='curso não encontrado')

@app.post('/cursos')
def post_cursos(curso: Cursos) -> dict:
    if curso.id in cursos:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Curso já existe! {curso}')
    next_id = len(cursos) + 1 if curso.id is None else curso.id
    cursos[next_id] = curso
    cursos[next_id].id = next_id
    return cursos[next_id]
        
@app.put('/cursos/{curso_id}')
def put_cursos(curso_id: int, curso: Cursos, request: Any = Depends(choices)) -> dict:
    if curso_id in cursos:
        cursos[curso_id] = curso
        return cursos[curso_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Curso id {curso_id} nao foi encontrado')

@app.delete('/cursos/{curso_id}')    
def delete_cursos(curso_id: int, request: Any = Depends(choices)) -> dict:
    if curso_id in cursos:
        curso = cursos[curso_id]
        del cursos[curso_id]
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