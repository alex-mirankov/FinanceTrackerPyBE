from pydantic import BaseModel

class TransactionCategoryCreate(BaseModel):
    name: str
    type: str

class TransactionCategoryResponse(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        orm_mode = True