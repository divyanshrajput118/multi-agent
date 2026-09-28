from pydantic import BaseModel

class InputSchema(BaseModel):
    topic: str

