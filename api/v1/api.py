from fastapi import APIRouter

from api.v1 import artigos
from api.v1 import usuarios


router = APIRouter()

router.include_router(artigos.router, prefix='/artigos', tags=['artigos'])
router.include_router(usuarios.router, prefix='/usuarios', tags=['usuarios'])