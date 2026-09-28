"""Importa todos os models para que o Alembic os enxergue."""
from workout_api.atleta.models import Atleta  # noqa: F401
from workout_api.categorias.models import Categoria  # noqa: F401
from workout_api.centro_treinamento.models import CentroTreinamento  # noqa: F401
from workout_api.contrib.models import Base  # noqa: F401
