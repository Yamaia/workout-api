from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status
from fastapi_pagination import LimitOffsetPage
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select

from workout_api.atleta.models import Atleta
from workout_api.atleta.schemas import AtletaIn, AtletaListOut, AtletaOut, AtletaUpdate
from workout_api.categorias.models import Categoria
from workout_api.centro_treinamento.models import CentroTreinamento
from workout_api.configs.database import DBSession
from workout_api.contrib.errors import commit_or_conflict

router = APIRouter()


@router.post("/", summary="Criar atleta", status_code=status.HTTP_201_CREATED, response_model=AtletaOut)
async def criar(session: DBSession, body: AtletaIn) -> AtletaOut:
    categoria = await session.scalar(select(Categoria).where(Categoria.nome == body.categoria.nome))
    if categoria is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"A categoria {body.categoria.nome} não foi encontrada.")

    centro = await session.scalar(
        select(CentroTreinamento).where(CentroTreinamento.nome == body.centro_treinamento.nome)
    )
    if centro is None:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"O centro de treinamento {body.centro_treinamento.nome} não foi encontrado.",
        )

    atleta = Atleta(
        **body.model_dump(exclude={"categoria", "centro_treinamento"}),
        categoria=categoria,
        centro_treinamento=centro,
    )
    session.add(atleta)
    await commit_or_conflict(session, f"Já existe um atleta cadastrado com o cpf: {body.cpf}")
    return atleta


@router.get("/", summary="Listar atletas", response_model=LimitOffsetPage[AtletaListOut])
async def listar(
    session: DBSession,
    nome: Annotated[Optional[str], Query(description="Filtra por nome (contém, sem diferenciar maiúsculas)")] = None,
    cpf: Annotated[Optional[str], Query(description="Filtra pelo CPF exato")] = None,
):
    query = select(Atleta).order_by(Atleta.nome)
    if nome:
        query = query.where(Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.where(Atleta.cpf == cpf)
    return await apaginate(session, query)


async def _obter(session: DBSession, id: UUID) -> Atleta:
    atleta = await session.get(Atleta, id)
    if atleta is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Atleta não encontrado no id: {id}")
    return atleta


@router.get("/{id}", summary="Buscar atleta por id", response_model=AtletaOut)
async def buscar(id: UUID, session: DBSession) -> AtletaOut:
    return await _obter(session, id)


@router.patch("/{id}", summary="Editar atleta", response_model=AtletaOut)
async def editar(id: UUID, session: DBSession, body: AtletaUpdate) -> AtletaOut:
    atleta = await _obter(session, id)
    for campo, valor in body.model_dump(exclude_unset=True).items():
        setattr(atleta, campo, valor)
    await commit_or_conflict(session, "Não foi possível atualizar o atleta.")
    return atleta


@router.delete("/{id}", summary="Remover atleta", status_code=status.HTTP_204_NO_CONTENT)
async def remover(id: UUID, session: DBSession) -> None:
    atleta = await _obter(session, id)
    await session.delete(atleta)
    await session.commit()
