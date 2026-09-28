from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select

from workout_api.centro_treinamento.models import CentroTreinamento
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.configs.database import DBSession
from workout_api.contrib.errors import commit_or_conflict

router = APIRouter()


@router.post("/", summary="Criar centro de treinamento", status_code=status.HTTP_201_CREATED,
             response_model=CentroTreinamentoOut)
async def criar(session: DBSession, body: CentroTreinamentoIn) -> CentroTreinamentoOut:
    centro = CentroTreinamento(**body.model_dump())
    session.add(centro)
    await commit_or_conflict(
        session, f"Já existe um centro de treinamento cadastrado com o nome: {body.nome}"
    )
    return centro


@router.get("/", summary="Listar centros de treinamento", response_model=LimitOffsetPage[CentroTreinamentoOut])
async def listar(session: DBSession):
    return await apaginate(session, select(CentroTreinamento).order_by(CentroTreinamento.nome))


@router.get("/{id}", summary="Buscar centro de treinamento por id", response_model=CentroTreinamentoOut)
async def buscar(id: UUID, session: DBSession) -> CentroTreinamentoOut:
    centro = await session.get(CentroTreinamento, id)
    if centro is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Centro de treinamento não encontrado no id: {id}")
    return centro
