"""
Transaction categories entity module for Finance Tracker API.

This module provides API endpoints for managing transaction categories in the
Finance Tracker application. Transaction categories are used to classify
and organize transactions into meaningful groups (e.g., 'Food', 'Transportation',
'Salary', 'Rent') for better financial tracking and analysis.

Endpoints:
- GET /api/v1/transaction-category/: Retrieve all transaction categories for the authenticated user
- POST /api/v1/transaction-category/: Create a new transaction category
"""

from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from db.connect import get_db
from typing import List
from db.models.transaction_categories_model import TransactionCategory
from schemas.transaction_category_schema import (
    TransactionCategoryResponse,
    TransactionCategoryCreate,
)

router = APIRouter(
    prefix="/api/v1/transaction-category", tags=["Transaction Categories"]
)


@router.get("/", response_model=List[TransactionCategoryResponse])
def get_transaction_categories(request: Request, db: Session = Depends(get_db)):
    """
    Retrieve all transaction categories for the authenticated user.

    This endpoint returns a list of all transaction categories associated with
    the authenticated user. Transaction categories are used to classify
    transactions into meaningful groups for better financial organization.

    Args:
        request (Request): The HTTP request object containing user authentication info
        db (Session): Database session dependency for data access

    Returns:
        List[TransactionCategoryResponse]: List of transaction categories with their details

    Raises:
        HTTPException: 500 Internal Server Error if database operation fails

    Example:
        GET /api/v1/transaction-category/
        Returns: [
            {
                "id": 1,
                "name": "Food",
                "type": "expense"
            },
            {
                "id": 2,
                "name": "Salary",
                "type": "income"
            }
        ]
    """
    try:
        user = request.state.user_info
        return db.query(TransactionCategory).filter_by(user_id=user["id"]).all()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post("/", response_model=TransactionCategoryResponse)
def create_transaction_categories(
    category: TransactionCategoryCreate, request: Request, db: Session = Depends(get_db)
):
    """
    Create a new transaction category for the authenticated user.

    This endpoint creates a new transaction category with the specified name
    and type. Transaction categories help organize transactions into meaningful
    groups for better financial tracking and analysis.

    Args:
        category (TransactionCategoryCreate): The category data including name and type
        request (Request): The HTTP request object containing user authentication info
        db (Session): Database session dependency for data access

    Returns:
        TransactionCategoryResponse: The created transaction category with generated ID

    Raises:
        HTTPException: 500 Internal Server Error if database operation fails

    Example:
        POST /api/v1/transaction-category/
        Body: {
            "name": "Transportation",
            "type": "expense"
        }
        Returns: {
            "id": 3,
            "name": "Transportation",
            "type": "expense"
        }
    """
    user = request.state.user_info
    try:
        new_category = TransactionCategory(
            user_id=user["id"],
            name=category.name,
            type=category.type,
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return TransactionCategoryResponse(
            id=new_category.id,
            name=new_category.name,
            type=new_category.type,
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
