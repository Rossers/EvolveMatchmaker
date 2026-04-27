setup:
	copy .env.example .env

start:
	docker compose up --build

stop:
	docker compose down

restart:
	docker compose down
	docker compose up --build

logs:
	docker compose logs -f

format:
	docker compose run --rm api ruff format .

lint:
	docker compose run --rm api ruff check .

check:
	docker compose run --rm api ruff format --check .
	docker compose run --rm api ruff check .