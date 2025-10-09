from pydantic import BaseModel

class ApiKeyRequest(BaseModel):
    name: str