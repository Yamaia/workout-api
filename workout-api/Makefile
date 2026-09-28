run:
	uvicorn workout_api.main:app --reload

run-docker:
	docker compose up -d

create-migrations:
	alembic revision --autogenerate -m "$(d)"

run-migrations:
	alembic upgrade head

test:
	pytest -v
