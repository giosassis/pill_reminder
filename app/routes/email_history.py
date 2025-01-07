from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db_connection  
from app.models.email_history import EmailHistory
router = APIRouter()

@router.get("/email_history/")
def get_email_history(db: Session = Depends(get_db_connection), page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    email_history = db.query(EmailHistory).offset(skip).limit(page_size).all()

    return email_history
