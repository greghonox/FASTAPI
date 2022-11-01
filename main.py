from fastapi import FastAPI
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
    return aulas.get(curso_id, {1: {'titulo': 'Nao tem'}})

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', 
                port=8000, log_level='info', reload=True, debug=True)