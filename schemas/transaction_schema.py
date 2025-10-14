from datetime import datetime
from pydantic import BaseModel

class TransactionCreate(BaseModel):
    categoryId: int
    date: datetime
    amount: float
    comment: str
    type: str

class TransactionCreateResponse(BaseModel):
    id: int
    category_id: int
    date: datetime
    amount: float
    comment: str
    type: str

class TransactionResponse(BaseModel):
    id: int
    categoryId: int
    date: datetime
    amount: float
    comment: str
    type: str

    class Config:
        orm_mode = True