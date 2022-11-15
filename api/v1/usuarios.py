from typing import List
from fastapi import APIRouter, Depends, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from schemas.usuarios import Usuarios, UsuarioSchema, UsuarioSchemaArtigos, UsuarioSchemaUpdate, UsuarioSchema
from models.usuarios import Usuarios as UsuarioModel
from core.deps import get_session, get_current_user
from core.auth import autenticar, criar_token_acesso
from core.security import gerar_hash


router = APIRouter()

@router.get('/logado', response_model=Usuarios)
async def get(usuario: Usuarios = Depends(get_current_user)):
    return usuario

@router.post('/signup', status_code=status.HTTP_201_CREATED, 
            response_model=UsuarioSchema)
async def post(usuario: UsuarioSchema, db: AsyncSession = Depends(get_session)):
    try:
        novo_usuario = UsuarioModel(nome=usuario.nome, sobrenome=usuario.sobrenome,
                                    email=usuario.email, senha=gerar_hash(usuario.senha), admin=usuario.admin)
        async with db as session:
            session.add(novo_usuario)
            await session.commit()
            return novo_usuario

    except IntegrityError:
        raise HTTPException(detail=f'Erro em tentar criar usuario {usuario}',
                            status_code=status.HTTP_409_CONFLICT)

@router.get('/', response_model=List[Usuarios], status_code=status.HTTP_200_OK)
async def get(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchema] = result.scalars().unique().all()
        return usuarios
        
@router.get('/{usuario_id}', response_model=Usuarios, status_code=status.HTTP_200_OK)
async def get_usuarios(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()
        if usuario:
            return usuario
        HTTPException(detail=f'Usuario {usuario_id} nao encontrado', status_code=status.HTTP_404_NOT_FOUND)

@router.put('/{usuario_id}', status_code=status.HTTP_202_ACCEPTED)
async def put(usuario_id: int, usuario: UsuarioSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_up: UsuarioSchema = result.scalars().unique().one_or_none()
        if usuario_up:
            usuario_up.admin = usuario.admin
            usuario_up.nome = usuario.nome if usuario.nome else usuario_up.nome
            usuario_up.email = gerar_hash(usuario.email) if usuario.email else usuario_up.email
            usuario_up.sobrenome = usuario.sobrenome if usuario.sobrenome else usuario_up.sobrenome
            await session.commit()
            return usuario_up
        HTTPException(detail=f'Usuario {usuario_id} nao encontrado', status_code=status.HTTP_404_NOT_FOUND)        

@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchema = result.scalars().unique().one_or_none()
        if usuario:
            await session.delete(usuario)
            await session.commit()
            return usuario
        HTTPException(detail=f'Usuario {usuario_id} nao encontrado', status_code=status.HTTP_404_NOT_FOUND)              
        
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)
    if usuario:
        return JSONResponse(content={'token': criar_token_acesso(sub=usuario.id), 'token_type': 'bearer'}, 
                            status_code=status.HTTP_200_OK)
    raise HTTPException(details=f'Dados de acesso incorreto {form_data}')
    