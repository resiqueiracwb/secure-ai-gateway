# API Endpoints

---

## GET /health

### Purpose
Health check endpoint

### Response

{
  "status": "ok"
}

---

## POST /ai/prompt

### Purpose
Process AI prompt requests

### Request

{
  "prompt": "Explain FastAPI",
  "provider": "openai"
}

### Response

{
  "message": "Prompt processed"
}