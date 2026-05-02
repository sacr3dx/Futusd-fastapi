from pydantic import BaseModel

class SpendingSchema(BaseModel):
    base: int
    category: str
    date: int