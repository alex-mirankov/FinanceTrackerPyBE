from typing import List
from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from db.models.finance_periods_model import FinancePeriod
from db.models.transaction_categories_model import TransactionCategory
from db.models.transaction_model import Transaction
from db.connect import get_db
from schemas.pagination_schema import Pagination
from schemas.transaction_schema import TransactionCreate, TransactionCreateResponse, TransactionResponse

router = APIRouter(
    prefix='/api/v1/transactions',
    tags=['Posts']
)

@router.get('/', response_model=Pagination)
def get_transactions(request: Request, db: Session = Depends(get_db), periodId: int = 0, page: int = 0, size: int = 20, categoryId: int = 0):
    user = request.state.user_info
    transaction_query = db.query(Transaction, TransactionCategory).join(TransactionCategory).filter_by(user_id=user["id"])
    if periodId is not 0:
        period = db.query(FinancePeriod).filter_by(id=periodId).all()
        date_start = period[0].date_start
        date_end = period[0].date_end
        transaction_query = transaction_query.filter(Transaction.date >= date_start).filter(Transaction.date <= date_end).offset(page * size).limit(size).all()

    if categoryId is not 0:
        transaction_query = transaction_query.filter(TransactionCategory.id==categoryId)

    transactions = transaction_query.offset(page * size).limit(size).all()
    transaction_content = []
    total_count = db.query(Transaction).count()

    for transaction in transactions:
        transaction_content.append(
            TransactionResponse(
                id=transaction[0].id,
                category={"name": transaction[1].name, "id": transaction[1].id },
                date=transaction[0].date,
                amount=transaction[0].amount,
                comment=transaction[0].comment,
                type=transaction[0].type,
            )
        )
    return Pagination(content=transaction_content, totalCount=total_count, page=page, size=size)

@router.post('/', response_model=TransactionCreateResponse)
def create_transaction(transaction: TransactionCreate, request: Request, db: Session = Depends(get_db)):
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
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )
