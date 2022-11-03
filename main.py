from routes import cursos
from fastapi import FastAPI
from uvicorn import run

app = FastAPI()
app.include_router(cursos.route, tags=['cursos'])


if __name__ == '__main__':
    run('main:app', host='0.0.0.0', port=8000, debug=True, reload=True)