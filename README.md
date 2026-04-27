# EvolveMatchmaker

A Python backend service for matching 4 Hunters against 1 Monster.

This project will be built with FastAPI, PostgreSQL, Docker, and pytest. It is designed as a portfolio-friendly backend project focused on API design, matchmaking logic, database transactions, and scalable service architecture to demonstrate my python knowledge, coding style, and API design.

## Planned Features

- Players can join and leave a matchmaking queue
- Players are grouped by role: Hunter or Monster
- Matchmaking creates 4v1 matches with 4 hunters vs 1 monster (like Evolve)
- PostgreSQL persistence
- Docker Compose local development
- Optional local scaling with multiple API containers behind Nginx
- Automated tests with pytest

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy or SQLModel
- Docker
- Docker Compose
- pytest
