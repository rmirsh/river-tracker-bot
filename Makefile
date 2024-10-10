generate:
	alembic revision --m="$(name)" --autogenerate


migrate:
	alembic upgrade head