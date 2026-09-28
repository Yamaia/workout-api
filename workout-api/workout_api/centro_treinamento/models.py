from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from workout_api.contrib.models import Base, UUIDMixin


class CentroTreinamento(UUIDMixin, Base):
    __tablename__ = "centros_treinamento"

    nome: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    endereco: Mapped[str] = mapped_column(String(60), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(30), nullable=False)
