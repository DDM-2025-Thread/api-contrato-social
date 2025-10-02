from pydantic import BaseModel

class GenericResponse(BaseModel):
    message: str
    data: dict | None = None
    error: str | None = None