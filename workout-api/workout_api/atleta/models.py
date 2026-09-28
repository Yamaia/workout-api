import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from workout_api.categorias.models import Categoria
from workout_api.centro_treinamento.models import CentroTreinamento
from workout_api.contrib.models import Base, UUIDMixin


class Atleta(UUIDMixin, Base):
    __tablename__ = "atletas"

    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

    categoria_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("categorias.id"), nullable=False)
    categoria: Mapped[Categoria] = relationship(lazy="selectin")

    centro_treinamento_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("centros_treinamento.id"), nullable=False
    )
    centro_treinamento: Mapped[CentroTreinamento] = relationship(lazy="selectin")
