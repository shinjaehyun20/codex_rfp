SHELL := /bin/bash

.PHONY: up down api worker web test seed

up:
	docker compose up -d postgres redis minio

down:
	docker compose down -v

api:
	PYTHONPATH=. uvicorn apps.api.app.main:app --reload --host 0.0.0.0 --port 8000

worker:
	PYTHONPATH=. celery -A apps.worker.worker.celery_app.celery_app worker --loglevel=info

web:
	npm --prefix apps/web run dev

test:
	PYTHONPATH=. pytest -q

seed:
	@echo "Seed not implemented yet."
