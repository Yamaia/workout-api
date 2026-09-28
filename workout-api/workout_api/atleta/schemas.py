from datetime import datetime
from typing import Annotated, Literal, Optional
from uuid import UUID

from pydantic import Field, PositiveFloat, PositiveInt, StringConstraints, field_validator

from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema

Cpf = Annotated[str, StringConstraints(pattern=r"^\d{11}$"),
                Field(description="CPF do atleta (11 dígitos)", examples=["12345678900"])]


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", examples=["Joao"], min_length=1, max_length=50)]
    cpf: Cpf
    idade: Annotated[PositiveInt, Field(description="Idade", examples=[25])]
    peso: Annotated[PositiveFloat, Field(description="Peso em kg", examples=[75.5])]
    altura: Annotated[PositiveFloat, Field(description="Altura em metros", examples=[1.70])]
    sexo: Annotated[Literal["M", "F"], Field(description="Sexo", examples=["M"])]


class AtletaIn(Atleta):
    categoria: CategoriaIn
    centro_treinamento: CentroTreinamentoAtleta


class AtletaOut(Atleta):
    id: UUID
    created_at: datetime
    categoria: CategoriaIn
    centro_treinamento: CentroTreinamentoAtleta


class AtletaListOut(BaseSchema):
    """Resposta customizada do get all: apenas nome, centro de treinamento e categoria."""

    nome: str
    centro_treinamento: str
    categoria: str

    @field_validator("centro_treinamento", "categoria", mode="before")
    @classmethod
    def _extrair_nome(cls, valor):
        return getattr(valor, "nome", valor)


class AtletaUpdate(BaseSchema):
    nome: Optional[Annotated[str, Field(min_length=1, max_length=50)]] = None
    idade: Optional[PositiveInt] = None
