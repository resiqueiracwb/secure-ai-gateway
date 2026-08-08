# Pydantic Notes

## BaseModel

Used for validation and serialization.

---

## Field()

Adds validation rules.

Example:
Field(min_length=5)

---

## Optional

Optional[str]

Allows nullable fields.

---

## Nested Models

Models can contain other models.

Useful for:
- metadata
- complex payloads