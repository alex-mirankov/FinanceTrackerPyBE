from typing import List
from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from db.connect import get_db
from db.models.finance_periods_model import FinancePeriod
from schemas.finance_period_schema import FinancePeriodCreateResponse, FinancePeriodResponse, FinancePeriodCreate

router = APIRouter(
    prefix='/api/v1/finance-period',
    tags=['Finance Periods']
)

@router.get('/', response_model=List[FinancePeriodResponse])
def get_finance_period(request: Request, db: Session = Depends(get_db)):
    user = request.state.user_info
    periods = db.query(FinancePeriod).filter_by(user_id=user["id"]).all()
    return [
        FinancePeriodResponse(
            id=period.id,
            startDate=period.date_start,
            endDate=period.date_end,
            name=period.name
        )
        for period in periods
    ]

@router.post('/', response_model=FinancePeriodCreateResponse)
def create_finance_period(period: FinancePeriodCreate,request: Request, db: Session = Depends(get_db)):
    try:
        user = request.state.user_info
        new_period = FinancePeriod(
            user_id=user["id"],
            name=period.name,
            date_start=period.startDate,
            date_end=period.endDate
        )
        db.add(new_period)
        db.commit()
        db.refresh(new_period)

        return FinancePeriodCreateResponse(
            id=new_period.id,
            name=new_period.name,
            startDate=new_period.date_start,
            endDate=new_period.date_end,
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
