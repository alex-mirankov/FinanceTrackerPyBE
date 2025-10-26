from fastapi import APIRouter, HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from db.connect import get_db
from db.models.users_model import User

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/")
def get_user(request: Request, db: Session = Depends(get_db)):
    try:
        user = request.state.user_info
        return db.query(User).filter_by(sub_id=user["sub_id"]).first()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
