"""
Transactions entity module for Finance Tracker API.

This module provides API endpoints for managing financial transactions in the
Finance Tracker application. Transactions represent individual financial
movements (income or expenses) with associated metadata like category, date,
amount, and comments. The module supports pagination and filtering by finance
periods and categories.

Endpoints:
- GET /api/v1/transactions/: Retrieve paginated transactions with optional filtering
- POST /api/v1/transactions/: Create a new transaction
"""

from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from db.models.finance_periods_model import FinancePeriod
from db.models.transaction_categories_model import TransactionCategory
from db.models.transaction_model import Transaction
from db.connect import get_db
from schemas.pagination_schema import Pagination
from schemas.transaction_schema import (
    TransactionCreate,
    TransactionCreateResponse,
    TransactionResponse,
)

router = APIRouter(prefix="/api/v1/transactions", tags=["Posts"])


@router.get("/", response_model=Pagination)
def get_transactions(
    request: Request,
    db: Session = Depends(get_db),
    periodId: int = 0,
    page: int = 0,
    size: int = 20,
    categoryId: int = 0,
):
    """
    Retrieve paginated transactions with optional filtering.

    This endpoint returns a paginated list of transactions for the authenticated
    user with optional filtering by finance period and category. Transactions
    are joined with their categories to provide complete information.

    Args:
        request (Request): The HTTP request object containing user authentication info
        db (Session): Database session dependency for data access
        periodId (int, optional): Filter by finance period ID (0 = no filter). Defaults to 0
        page (int, optional): Page number for pagination (0-based). Defaults to 0
        size (int, optional): Number of items per page. Defaults to 20
        categoryId (int, optional): Filter by category ID (0 = no filter). Defaults to 0

    Returns:
        Pagination: Paginated response containing transactions and metadata

    Raises:
        HTTPException: 500 Internal Server Error if database operation fails

    Example:
        GET /api/v1/transactions/?periodId=1&page=0&size=10&categoryId=2
        Returns: {
            "content": [
                {
                    "id": 1,
                    "category": {"name": "Food", "id": 2},
                    "date": "2024-01-15T10:30:00",
                    "amount": 25.50,
                    "comment": "Lunch at restaurant",
                    "type": "expense"
                }
            ],
            "totalCount": 150,
            "page": 0,
            "size": 10
        }
    """
    try:
        user = request.state.user_info
        transaction_query = (
            db.query(Transaction, TransactionCategory)
            .join(TransactionCategory)
            .filter_by(user_id=user["id"])
        )

        if periodId != 0:
            period = db.query(FinancePeriod).filter_by(id=periodId).first()
            if period:
                transaction_query = transaction_query.filter(
                    Transaction.date >= period.date_start,
                    Transaction.date <= period.date_end,
                )

        if categoryId != 0:
            transaction_query = transaction_query.filter(
                TransactionCategory.id == categoryId
            )

        total_count = transaction_query.count()

        transactions = transaction_query.offset(page * size).limit(size).all()
        transaction_content = []

        for transaction in transactions:
            transaction_content.append(
                TransactionResponse(
                    id=transaction[0].id,
                    category={"name": transaction[1].name, "id": transaction[1].id},
                    date=transaction[0].date,
                    amount=transaction[0].amount,
                    comment=transaction[0].comment,
                    type=transaction[0].type,
                )
            )
        return Pagination(
            content=transaction_content, totalCount=total_count, page=page, size=size
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.post("/", response_model=TransactionCreateResponse)
def create_transaction(
    transaction: TransactionCreate, request: Request, db: Session = Depends(get_db)
):
    """
    Create a new transaction for the authenticated user.

    This endpoint creates a new financial transaction with the specified
    details including category, date, amount, comment, and type. The transaction
    is associated with the authenticated user and linked to the specified category.

    Args:
        transaction (TransactionCreate): The transaction data including all required fields
        request (Request): The HTTP request object containing user authentication info
        db (Session): Database session dependency for data access

    Returns:
        TransactionCreateResponse: The created transaction with generated ID

    Raises:
        HTTPException: 500 Internal Server Error if database operation fails

    Example:
        POST /api/v1/transactions/
        Body: {
            "categoryId": 2,
            "date": "2024-01-15T10:30:00",
            "amount": 25.50,
            "comment": "Lunch at restaurant",
            "type": "expense"
        }
        Returns: {
            "id": 1,
            "category_id": 2,
            "date": "2024-01-15T10:30:00",
            "amount": 25.50,
            "comment": "Lunch at restaurant",
            "type": "expense"
        }
    """
    user = request.state.user_info
    try:
        new_transaction = Transaction(
            user_id=user["id"],
            category_id=transaction.categoryId,
            date=transaction.date,
            amount=transaction.amount,
            comment=transaction.comment,
            type=transaction.type,
        )

        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        return TransactionCreateResponse(
            id=new_transaction.id,
            category_id=new_transaction.category_id,
            date=new_transaction.date,
            amount=new_transaction.amount,
            comment=new_transaction.comment,
            type=new_transaction.type,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
