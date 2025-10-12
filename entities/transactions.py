from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.models.transaction_model import Transaction
from db.connect import get_db

router = APIRouter(
    prefix='/api/v1/transactions',
    tags=['Posts']
)

@router.get('/')
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()
