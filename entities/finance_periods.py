"""
Finance periods entity module for Finance Tracker API.

This module provides API endpoints for managing finance periods in the
Finance Tracker application. Finance periods represent time ranges
(e.g., monthly, quarterly, yearly) for organizing and tracking financial
data and transactions.

Endpoints:
- GET /api/v1/finance-period/: Retrieve all finance periods for the authenticated user
- POST /api/v1/finance-period/: Create a new finance period
"""

from typing import List
from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from db.connect import get_db
from db.models.finance_periods_model import FinancePeriod
from schemas.finance_period_schema import (
    FinancePeriodCreateResponse,
    FinancePeriodResponse,
    FinancePeriodCreate,
)

router = APIRouter(prefix="/api/v1/finance-period", tags=["Finance Periods"])


@router.get("/", response_model=List[FinancePeriodResponse])
def get_finance_period(request: Request, db: Session = Depends(get_db)):
    """
    Retrieve all finance periods for the authenticated user.

    This endpoint returns a list of all finance periods associated with
    the authenticated user. Finance periods are used to organize financial
    data into specific time ranges for better tracking and analysis.

    Args:
        request (Request): The HTTP request object containing user authentication info
        db (Session): Database session dependency for data access

    Returns:
        List[FinancePeriodResponse]: List of finance periods with their details

    Raises:
        HTTPException: 500 Internal Server Error if database operation fails

    Example:
        GET /api/v1/finance-period/
        Returns: [
            {
                "id": 1,
                "startDate": "2024-01-01T00:00:00",
                "endDate": "2024-01-31T23:59:59",
                "name": "January 2024"
            }
        ]
    """
    try:
        user = request.state.user_info
        periods = db.query(FinancePeriod).filter_by(user_id=user["id"]).all()
        return [
            FinancePeriodResponse(
                id=period.id,
                startDate=period.date_start,
                endDate=period.date_end,
                name=period.name,
            )
            for period in periods
        ]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post("/", response_model=FinancePeriodCreateResponse)
def create_finance_period(
    period: FinancePeriodCreate, request: Request, db: Session = Depends(get_db)
):
    """
    Create a new finance period for the authenticated user.

    This endpoint creates a new finance period with the specified time range
    and name. Finance periods help organize financial data into meaningful
    time segments for tracking and analysis.

    Args:
        period (FinancePeriodCreate): The finance period data including name and date range
        request (Request): The HTTP request object containing user authentication info
        db (Session): Database session dependency for data access

    Returns:
        FinancePeriodCreateResponse: The created finance period with generated ID

    Raises:
        HTTPException: 500 Internal Server Error if database operation fails

    Example:
        POST /api/v1/finance-period/
        Body: {
            "name": "Q1 2024",
            "startDate": "2024-01-01T00:00:00",
            "endDate": "2024-03-31T23:59:59"
        }
        Returns: {
            "id": 1,
            "name": "Q1 2024",
            "startDate": "2024-01-01T00:00:00",
            "endDate": "2024-03-31T23:59:59"
        }
    """
    try:
        user = request.state.user_info
        new_period = FinancePeriod(
            user_id=user["id"],
            name=period.name,
            date_start=period.startDate,
            date_end=period.endDate,
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
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
