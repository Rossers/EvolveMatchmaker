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

queue-join-hunter-high:
	curl.exe -X POST http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_hunter_high.json

queue-join-hunter-low:
	curl.exe -X POST http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_hunter_low.json

queue-join-monster-high:
	curl.exe -X POST http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_monster_high.json

queue-join-monster-low:
	curl.exe -X POST http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_monster_low.json

queue-fetch:
	powershell -Command "Invoke-RestMethod -Uri http://localhost:8080/queue"