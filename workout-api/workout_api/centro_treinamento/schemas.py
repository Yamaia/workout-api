from typing import Annotated
from uuid import UUID

from pydantic import Field

from workout_api.contrib.schemas import BaseSchema


class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", examples=["CT King"], min_length=1, max_length=20)]
    endereco: Annotated[str, Field(description="Endereço", examples=["Rua X, Q02"], min_length=1, max_length=60)]
    proprietario: Annotated[str, Field(description="Proprietário", examples=["Marcos"], min_length=1, max_length=30)]


class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", examples=["CT King"], max_length=20)]


class CentroTreinamentoOut(CentroTreinamentoIn):
    id: UUID
