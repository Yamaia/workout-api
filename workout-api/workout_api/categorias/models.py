from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from workout_api.contrib.models import Base, UUIDMixin


class Categoria(UUIDMixin, Base):
    __tablename__ = "categorias"

    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
