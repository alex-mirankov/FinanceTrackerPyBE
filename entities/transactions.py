from typing import List
from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from db.models.transaction_model import Transaction
from db.connect import get_db
from schemas.transaction_schema import TransactionCreate, TransactionCreateResponse, TransactionResponse

router = APIRouter(
    prefix='/api/v1/transactions',
    tags=['Posts']
)

@router.get('/', response_model=List[TransactionResponse])
def get_transactions(request: Request, db: Session = Depends(get_db)):
    user = request.state.user_info
    transactions = db.query(Transaction).filter_by(user_id=user["id"]).all()
    return [
        TransactionResponse(
            id=transaction.id,
            categoryId=transaction.category_id,
            date=transaction.date,
            amount=transaction.amount,
            comment=transaction.comment,
            type=transaction.type,
        ) for transaction in transactions
    ]

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
