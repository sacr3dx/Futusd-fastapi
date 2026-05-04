from pydantic import BaseModel
from datetime import date

class SpendingSchema(BaseModel):
    base: int
    category: str
    date: date