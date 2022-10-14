from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/')
async def raiz() -> dict:
    return {'msg': 'MSG INIT'}

@app.get('/mensagem')
async def message() -> str:
    return 'message fastapi'

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', 
                port=8000, log_level='info', reload=True)