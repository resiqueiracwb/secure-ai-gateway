# Architecture

Secure AI Gateway is organized as a layered FastAPI backend. The application exposes HTTP endpoints, validates requests with Pydantic models, protects AI routes with JWT authentication and role-based authorization, persists users in PostgreSQL, and keeps database schema changes under Alembic migrations.

## System Overview

```mermaid
flowchart LR
    Client["Client / API Consumer"] --> API["FastAPI Application"]
    API --> Middleware["Request Middleware"]
    Middleware --> Routes["Routes"]
    Routes --> Security["Security Layer"]
    Routes --> Services["Service Layer"]
    Routes --> Repositories["Repository Layer"]
    Repositories --> DB["PostgreSQL"]
    Services --> AIProviders["AI Provider Abstraction"]
```

The current AI implementation normalizes prompts locally, but the service layer is designed as the future integration point for external providers such as OpenAI, Claude, and Gemini.

## Runtime Components

### FastAPI Application

Entry point:

```text
app/main.py
```

Responsibilities:

- create the FastAPI app
- configure application metadata
- register routers
- register middleware
- register custom exception handlers

Registered routers:

```text
/auth
/ai
/health
```

### PostgreSQL

PostgreSQL stores user records used by the authentication flow.

Main entity:

```text
app/entities/user_entity.py
```

Current table:

```text
users
```

Expected columns:

```text
id
username
password
role
```

### Alembic

Alembic manages schema migrations.

Important files:

```text
alembic.ini
alembic/env.py
alembic/versions/
```

Run migrations:

```bash
alembic upgrade head
```

## Application Layers

```mermaid
flowchart TB
    Routes["routes/"] --> Models["models/"]
    Routes --> Security["security/"]
    Routes --> Services["services/"]
    Routes --> Repositories["repositories/"]
    Repositories --> Database["database/"]
    Database --> Entities["entities/"]
    Routes --> Exceptions["exceptions/"]
    Middleware["middleware/"] --> Utils["utils/"]
```

### `routes/`

The route layer handles HTTP concerns:

- endpoint paths
- request parsing
- response status codes
- dependency injection
- calling services or repositories

Main route modules:

```text
app/routes/auth.py
app/routes/ai.py
app/routes/health.py
```

### `models/`

The model layer contains Pydantic schemas for input validation and response shaping.

Examples:

```text
LoginRequest
PromptRequest
PromptResponse
```

The AI prompt model validates:

- prompt length
- provider enum
- temperature range
- max token range
- optional tags
- optional metadata

Supported providers:

```text
openai
claude
gemini
```

### `security/`

The security layer handles authentication and authorization.

Responsibilities:

- password hashing and verification
- JWT creation
- JWT validation
- extracting the current user from bearer tokens
- enforcing admin-only access

Important modules:

```text
app/security/password_handler.py
app/security/jwt_handler.py
app/security/dependencies.py
app/security/authorization.py
```

Security behavior:

- missing or invalid token returns `401 Unauthorized`
- authenticated non-admin users return `403 Forbidden` on admin-only routes

### `services/`

The service layer contains business logic that should not live directly in HTTP route handlers.

Current service:

```text
app/services/ai_service.py
```

Current behavior:

- validates that the provider is supported
- normalizes the prompt by trimming whitespace and uppercasing it

Future AI provider integrations should be added behind this layer so routes remain stable.

### `repositories/`

The repository layer isolates database queries from routes and services.

Current repository:

```text
app/repositories/user_repository.py
```

Current responsibility:

- find a user by username

### `database/`

The database layer owns SQLAlchemy setup.

Important modules:

```text
app/database/connection.py
app/database/session.py
app/database/dependencies.py
app/database/base.py
```

Responsibilities:

- create the SQLAlchemy engine
- configure database sessions
- provide FastAPI database dependencies
- expose declarative base metadata

### `middleware/`

Middleware runs around every request.

Current middleware:

```text
RequestContextMiddleware
LoggingMiddleware
```

`RequestContextMiddleware`:

- creates a unique request ID
- stores it in `request.state.request_id`
- logs request start and completion
- adds `X-Request-ID` to the response
- records latency in milliseconds

`LoggingMiddleware`:

- logs request method and path
- logs request duration

### `exceptions/`

Custom exceptions keep domain errors explicit.

Current custom exception:

```text
ProviderNotSupportedException
```

When an unsupported provider reaches the AI service, the app returns:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_PROVIDER",
    "message": "Provider '<provider>' is not supported"
  }
}
```

### `utils/`

Shared utilities live here.

Current utility:

```text
app/utils/logger.py
```

The logger emits JSON logs to stdout so Docker, CI, and deployment platforms can collect structured logs.

## Authentication Flow

```mermaid
sequenceDiagram
    participant Client
    participant AuthRoute as /auth/login
    participant Repo as UserRepository
    participant DB as PostgreSQL
    participant JWT as jwt_handler

    Client->>AuthRoute: POST username/password
    AuthRoute->>Repo: get_by_username(username)
    Repo->>DB: SELECT user
    DB-->>Repo: user
    Repo-->>AuthRoute: user
    AuthRoute->>AuthRoute: verify password
    AuthRoute->>JWT: create_access_token()
    JWT-->>AuthRoute: signed JWT
    AuthRoute-->>Client: access_token
```

## Protected AI Prompt Flow

```mermaid
sequenceDiagram
    participant Client
    participant AIRoute as /ai/prompt
    participant Security as Security Dependencies
    participant Service as AIService

    Client->>AIRoute: POST prompt with Bearer token
    AIRoute->>Security: validate token and require admin
    Security-->>AIRoute: current user payload
    AIRoute->>Service: process_prompt(prompt, provider)
    Service-->>AIRoute: normalized prompt
    AIRoute-->>Client: PromptResponse
```

## Health Checks

Health endpoints are grouped under `/health`.

```text
GET /health
GET /health/live
GET /health/ready
```

Responsibilities:

- `/health` returns a general healthy status
- `/health/live` confirms the application process is alive
- `/health/ready` checks database connectivity with `SELECT 1`

## Configuration

Application configuration is centralized in:

```text
app/core/settings.py
```

Settings are loaded from environment variables and `.env` using Pydantic Settings.

Required settings:

```text
APP_NAME
APP_VERSION
DATABASE_URL
JWT_SECRET
```

Optional settings:

```text
DEBUG
```

Database URLs differ by runtime environment:

```text
Docker Compose: postgresql://admin:admin@postgres:5432/secure_ai_gateway
Host machine:   postgresql://admin:admin@localhost:5432/secure_ai_gateway
GitHub Actions: postgresql://admin:admin@localhost:5432/secure_ai_gateway
```

## Deployment Model

Local Docker Compose runs two services:

```text
api
postgres
```

The API container listens on port `8000`. Docker exposes it on the host at port `8001`.

```text
Host:      http://localhost:8001
Container: http://api:8000
```

The API reaches PostgreSQL through Docker's internal network using:

```text
postgres:5432
```

## Testing Architecture

Tests live in:

```text
app/tests/
```

Current test coverage includes:

- successful login
- AI prompt rejects missing authentication
- AI prompt succeeds with a valid admin token

The test configuration sets the database URL to `localhost:5432` because tests run from the host environment, not inside the Docker network.

```text
app/tests/conftest.py
```

## CI Architecture

GitHub Actions runs the test job with a PostgreSQL service container.

The database is exposed to the runner at:

```text
localhost:5432
```

The CI workflow sets:

```text
DATABASE_URL=postgresql://admin:admin@localhost:5432/secure_ai_gateway
```

CI steps:

1. Check out repository
2. Set up Python
3. Install dependencies
4. Wait for PostgreSQL
5. Run Alembic migrations
6. Seed test user
7. Run tests

## Design Principles

- Keep HTTP concerns in routes.
- Keep business behavior in services.
- Keep database queries in repositories.
- Keep schema validation in Pydantic models.
- Keep authentication and authorization in the security layer.
- Keep configuration environment-driven.
- Use structured logs for observability.
- Keep Docker, local development, and CI database URLs explicit.

## Current Limitations

- AI provider calls are not yet integrated with external APIs.
- The seeded admin user is intended for development and tests.
- JWT secret management is environment-based and should use a secret manager in production.
- Database migrations must be run before using a fresh database.
