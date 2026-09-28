# 🏋️ WorkoutAPI

![CI](https://github.com/SEU_USUARIO/workout-api/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-async-009688)

API assíncrona de competição de crossfit feita com **FastAPI**, **SQLAlchemy 2 (async)**, **Alembic**, **PostgreSQL** e **fastapi-pagination**.

Projeto do desafio final da [DIO](https://www.dio.me/), baseado em [digitalinnovationone/workout_api](https://github.com/digitalinnovationone/workout_api).

## Requisitos do desafio implementados

| Requisito | Implementação |
|---|---|
| Query parameters em atleta (`nome`, `cpf`) | `GET /atletas/?nome=joao&cpf=12345678900` (nome: contém, sem diferenciar maiúsculas; cpf: exato) |
| Response customizada no get all de atleta | Retorna apenas `nome`, `centro_treinamento` e `categoria` (`AtletaListOut`) |
| Tratamento de `sqlalchemy.exc.IntegrityError` | Status **303** com `Já existe um atleta cadastrado com o cpf: x`. Também em categorias e centros de treinamento |
| Paginação com `fastapi-pagination` | `limit` e `offset` em todas as listagens (`LimitOffsetPage`) |

### Exemplos
```bash
# get all customizado + paginação
curl "http://127.0.0.1:8000/atletas/?limit=10&offset=0"
```
```json
{
  "items": [{"nome": "Joao", "centro_treinamento": "CT King", "categoria": "Scale"}],
  "total": 1, "limit": 10, "offset": 0
}
```
```bash
# cpf duplicado
curl -X POST http://127.0.0.1:8000/atletas/ -H "Content-Type: application/json" -d '{...}'
# 303 -> {"detail": "Já existe um atleta cadastrado com o cpf: 12345678900"}
```

## Endpoints
| Recurso | Rotas |
|---|---|
| `/atletas` | `POST /`, `GET /` (filtros + paginação), `GET /{id}`, `PATCH /{id}`, `DELETE /{id}` |
| `/categorias` | `POST /`, `GET /` (paginado), `GET /{id}` |
| `/centros_treinamento` | `POST /`, `GET /` (paginado), `GET /{id}` |

Para criar um atleta, cadastre antes a categoria e o centro de treinamento, pois o payload os referencia pelo `nome`.

## Estrutura
```
workout_api/
  configs/            settings (DB_URL) e sessão async
  contrib/            Base, schemas base e tratamento de IntegrityError
  atleta/             models, schemas, controller
  categorias/         models, schemas, controller
  centro_treinamento/ models, schemas, controller
  main.py             app + paginação
alembic/              migrations (async)
tests/                testes com pytest (SQLite em memória)
```

## Como executar
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env

make run-docker        # sobe o PostgreSQL
make run-migrations    # cria as tabelas
make run               # http://127.0.0.1:8000/docs
```
Nova migration: `make create-migrations d="nome_da_migration"`.

## Testes
```bash
make test
```
Os testes usam SQLite em memória e cobrem criação, filtros, paginação, resposta customizada e os erros 303/400/404/422.

## Stack
FastAPI · SQLAlchemy 2 (async) · asyncpg · Alembic · Pydantic v2 · fastapi-pagination · pytest

## Licença
MIT
