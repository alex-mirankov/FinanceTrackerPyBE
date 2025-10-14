from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from db.connect import get_db
from typing import List
from db.models.transaction_categories_model import TransactionCategory
from schemas.transaction_category_schema import TransactionCategoryResponse, TransactionCategoryCreate

router = APIRouter(
    prefix='/api/v1/transaction-category',
    tags=['Transaction Categories']
)

@router.get('/', response_model=List[TransactionCategoryResponse])
def get_transaction_categories(request: Request, db: Session = Depends(get_db)):
    user = request.state.user_info
    return db.query(TransactionCategory).filter_by(user_id=user["id"]).all()

@router.post('/', response_model=TransactionCategoryResponse)
def create_transaction_categories(category: TransactionCategoryCreate,request: Request, db: Session = Depends(get_db)):
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
            detail="Internal Server Error"
        )
