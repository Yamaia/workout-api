import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from workout_api.configs.database import get_session
from workout_api.contrib.models import Base
from workout_api.main import app
import workout_api.models  # noqa: F401


@pytest_asyncio.fixture
async def client():
    engine = create_async_engine("sqlite+aiosqlite://", poolclass=StaticPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)

    async def override():
        async with maker() as session:
            yield session

    app.dependency_overrides[get_session] = override
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
    await engine.dispose()


def atleta_payload(**extra):
    base = {
        "nome": "Joao", "cpf": "12345678900", "idade": 25, "peso": 75.5, "altura": 1.7, "sexo": "M",
        "categoria": {"nome": "Scale"}, "centro_treinamento": {"nome": "CT King"},
    }
    base.update(extra)
    return base


async def preparar_base(client):
    r1 = await client.post("/categorias/", json={"nome": "Scale"})
    r2 = await client.post("/centros_treinamento/", json={"nome": "CT King", "endereco": "Rua X, Q02", "proprietario": "Marcos"})
    assert r1.status_code == 201 and r2.status_code == 201
