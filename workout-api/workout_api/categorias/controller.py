from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select

from workout_api.categorias.models import Categoria
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.configs.database import DBSession
from workout_api.contrib.errors import commit_or_conflict

router = APIRouter()


@router.post("/", summary="Criar categoria", status_code=status.HTTP_201_CREATED, response_model=CategoriaOut)
async def criar(session: DBSession, body: CategoriaIn) -> CategoriaOut:
    categoria = Categoria(**body.model_dump())
    session.add(categoria)
    await commit_or_conflict(session, f"Já existe uma categoria cadastrada com o nome: {body.nome}")
    return categoria


@router.get("/", summary="Listar categorias", response_model=LimitOffsetPage[CategoriaOut])
async def listar(session: DBSession):
    return await apaginate(session, select(Categoria).order_by(Categoria.nome))


@router.get("/{id}", summary="Buscar categoria por id", response_model=CategoriaOut)
async def buscar(id: UUID, session: DBSession) -> CategoriaOut:
    categoria = await session.get(Categoria, id)
    if categoria is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Categoria não encontrada no id: {id}")
    return categoria
