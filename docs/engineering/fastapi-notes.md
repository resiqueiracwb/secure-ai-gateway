# FastAPI Notes

## FastAPI App

app = FastAPI()

Creates the main application object.

---

## Swagger

/docs

Automatic API documentation.

---

## Routers

Used for modular APIs.

Example:
app.include_router()

---

## Dependency Injection

FastAPI supports Depends()

Useful for:
- services
- auth
- config