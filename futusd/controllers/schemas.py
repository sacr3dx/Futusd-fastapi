from pydantic import BaseModel, Field
from datetime import date

class SpendingCreateSchema(BaseModel):
    base: int = Field(gt=0, description="Spending amount")
    category: str = Field(min_length=1, max_length=20, description="Name of spending group")
    date: date

class SpendingResponseSchema(BaseModel):
    uuid: str
    base: int = Field(gt=0, description="Spending amount")
    category: str = Field(min_length=1, max_length=20, description="Name of spending group")
    date: date