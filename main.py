from fastapi import FastAPI, HTTPException, status
from models import Cursos
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
def get_cursos(curso_id: int) -> dict:
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

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', 
                port=8000, log_level='info', reload=True, debug=True)