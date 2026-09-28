from typing import Annotated
from uuid import UUID

from pydantic import Field

from workout_api.contrib.schemas import BaseSchema

Nome = Annotated[str, Field(description="Nome da categoria", examples=["Scale"], min_length=1, max_length=50)]


class CategoriaIn(BaseSchema):
    nome: Nome


class CategoriaOut(CategoriaIn):
    id: UUID
