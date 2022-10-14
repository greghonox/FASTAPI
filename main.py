from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def raiz() -> dict:
    return {'msg': 'MSG INIT'}