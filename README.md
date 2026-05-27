# Secure AI Gateway

Secure AI Gateway is a FastAPI backend for protected AI prompt processing. It includes JWT authentication, role-based authorization, PostgreSQL persistence, database migrations with Alembic, Docker Compose setup, request logging, and automated tests.

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL 16
- SQLAlchemy
- Alembic
- Pydantic Settings
- JWT authentication
- Docker Compose
- Pytest

## Project Structure

```text
app/
  core/          Application settings
  database/      SQLAlchemy engine, session, and dependencies
  entities/      Database entities
  middleware/    Logging and request context middleware
  models/        Pydantic request/response models
  repositories/  Data access layer
  routes/        API routes
  security/      JWT, password hashing, auth dependencies
  services/      Business logic
  tests/         Test suite
alembic/         Database migrations
docker-compose.yml
Dockerfile
seed_test_user.py
```

## Environment Variables

Create a `.env` file in the project root:

```env
APP_NAME=Secure AI Gateway
APP_VERSION=1.0.0
DATABASE_URL=postgresql://admin:admin@postgres:5432/secure_ai_gateway
JWT_SECRET=my-super-secret-key
DEBUG=true
```

For local commands outside Docker, use:

```env
DATABASE_URL=postgresql://admin:admin@localhost:5432/secure_ai_gateway
```

Inside Docker Compose, `postgres` is the correct database hostname. On your host machine, use `localhost`.

## Running With Docker

Build and start the API plus PostgreSQL:

```bash
docker compose up --build
```

The API runs inside the container on port `8000`, and Docker exposes it on your machine at:

```text
http://localhost:8001
```

Open the interactive API docs:

```text
http://localhost:8001/docs
```

Check service status:

```bash
docker compose ps
```

View API logs:

```bash
docker compose logs api
```

Stop the stack:

```bash
docker compose down
```

## Database Setup

Run migrations from your host machine:

```bash
alembic upgrade head
```

Seed the default test/admin user:

```bash
python seed_test_user.py
```

Default seeded credentials:

```text
username: renato
password: 123456
role: admin
```

## Local Development

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API locally:

```bash
uvicorn app.main:app --reload
```

When running locally outside Docker, make sure `DATABASE_URL` points to `localhost`, not `postgres`.

## API Endpoints

### Health

```http
GET /health
GET /health/live
GET /health/ready
```

### Authentication

```http
POST /auth/login
```

Request body:

```json
{
  "username": "renato",
  "password": "123456"
}
```

Response:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### AI Prompt

```http
POST /ai/prompt
```

Requires a bearer token from `/auth/login`.

Request body:

```json
{
  "prompt": "Explain FastAPI security",
  "provider": "openai",
  "temperature": 0.7,
  "max_tokens": 200,
  "tags": ["security", "fastapi"],
  "metadata": {
    "source": "docs",
    "priority": 3
  }
}
```

Supported providers:

```text
openai
claude
gemini
```

## Example Requests

Login:

```bash
curl -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"renato","password":"123456"}'
```

Call the AI prompt endpoint:

```bash
curl -X POST http://localhost:8001/ai/prompt \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"prompt":"Explain FastAPI security","provider":"openai"}'
```

## Running Tests

Run all tests:

```bash
pytest
```

Or with the project virtual environment:

```bash
.venv/bin/pytest -q app/tests
```

The tests expect a PostgreSQL database to be available at:

```text
postgresql://admin:admin@localhost:5432/secure_ai_gateway
```

## CI

GitHub Actions runs the test suite using a PostgreSQL service container. In CI, the database is exposed to the runner at `localhost:5432`, so the workflow sets:

```env
DATABASE_URL=postgresql://admin:admin@localhost:5432/secure_ai_gateway
```

## Notes

- Use `http://localhost:8001/docs` when running with Docker Compose.
- Use `docker compose logs api` for API logs. The Compose service name is `api`; the container name is `secure-ai-api`.
- A missing bearer token returns `401 Unauthorized`.
- A valid token without admin role returns `403 Forbidden`.
