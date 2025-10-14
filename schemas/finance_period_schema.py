from datetime import datetime
from pydantic import BaseModel

class FinancePeriodCreate(BaseModel):
    startDate: datetime
    endDate: datetime
    name: str

class FinancePeriodCreateResponse(BaseModel):
    id: int
    startDate: datetime
    endDate: datetime
    name: str

class FinancePeriodResponse(BaseModel):
    id: int
    startDate: datetime
    endDate: datetime
    name: str

    class Config:
        orm_mode = True