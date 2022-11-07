from core.configs import settings
from api.v1.api import api_router
from fastapi import FastAPI
from uvicorn import run


app: FastAPI = FastAPI(title='Cursos FastAPI com SQL Model')
app.include_router(api_router, prefix=settings.API_VERSION)

if __name__ == '__main__':
    run('main:app', host='0.0.0.0', port=8080,
        log_level='info', reload=True, debug=True)