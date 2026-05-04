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

fetch-queue:
	powershell -Command "Invoke-RestMethod -Uri http://localhost:8080/queue"

run-matchmaker:
	curl.exe -X POST http://localhost:8080/matchmaking/run

seed-match:
	curl.exe -X POST http://localhost:8080/queue/join -H "Content-Type: application/json" --data-binary @payloads/player_join_hunter_1.json
	curl.exe -X POST http://localhost:8080/queue/join -H "Content-Type: application/json" --data-binary @payloads/player_join_hunter_2.json
	curl.exe -X POST http://localhost:8080/queue/join -H "Content-Type: application/json" --data-binary @payloads/player_join_hunter_3.json
	curl.exe -X POST http://localhost:8080/queue/join -H "Content-Type: application/json" --data-binary @payloads/player_join_hunter_4.json
	curl.exe -X POST http://localhost:8080/queue/join -H "Content-Type: application/json" --data-binary @payloads/player_join_monster_2.json

clear-queue:
	curl.exe -X DELETE http://localhost:8080/dev/queue

fetch-matches:
	curl.exe http://localhost:8080/matches

join-h-1:
	curl.exe -X POST http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_hunter_1.json

join-h-2:
	curl.exe -X POST http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_hunter_2.json

join-h-3:
	curl.exe -X POST http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_hunter_3.json

join-h-4:
	curl.exe -X POST http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_hunter_4.json

join-h-5:
	curl.exe -X POST http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_hunter_5.json

join-m-1:
	curl.exe -X POST1 http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_monster_1.json

join-m-2:
	curl.exe -X POST http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_monster_2.json

join-m-3:
	curl.exe -X POST http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_monster_3.json

join-m-4:
	curl.exe -X POST http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_monster_4.json

join-m-5:
	curl.exe -X POST http://localhost:8080/queue/join \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_join_monster_5.json

leave-h-1:
	curl.exe -X POST http://localhost:8080/queue/leave \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_leave_hunter_1.json

leave-h-2:
	curl.exe -X POST http://localhost:8080/queue/leave \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_leave_hunter_2.json

leave-h-3:
	curl.exe -X POST http://localhost:8080/queue/leave \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_leave_hunter_3.json

leave-h-4:
	curl.exe -X POST http://localhost:8080/queue/leave \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_leave_hunter_4.json

leave-h-5:
	curl.exe -X POST http://localhost:8080/queue/leave \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_leave_hunter_5.json

leave-m-1:
	curl.exe -X POST http://localhost:8080/queue/leave \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_leave_monster_1.json

leave-m-2:
	curl.exe -X POST http://localhost:8080/queue/leave \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_leave_monster_2.json

leave-m-3:
	curl.exe -X POST http://localhost:8080/queue/leave \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_leave_monster_3.json

leave-m-4:
	curl.exe -X POST http://localhost:8080/queue/leave \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_leave_monster_4.json

leave-m-5:
	curl.exe -X POST http://localhost:8080/queue/leave \
	  -H "Content-Type: application/json" \
	  --data-binary @payloads/player_leave_monster_5.json