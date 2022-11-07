from fastapi import APIRouter
from api.v1.cursos import route as cursos

api_router:APIRouter = APIRouter()
api_router.include_router(cursos, tags=['cursos'])