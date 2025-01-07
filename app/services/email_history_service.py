from sqlalchemy.orm import Session
from app.models.email_history import EmailHistory
from app.utils.generate_history_id import generate_history_id
from datetime import datetime

def log_email_send(db: Session, recipient_email: str, status: str, subject: str, error_message: str = None):
    history_id = generate_history_id()
    
    email_history = EmailHistory(
        id=history_id,
        recipient_email=recipient_email,
        status=status,
        sent_at=datetime.utcnow(),
        subject=subject,
        error_message=error_message
    )

    db.add(email_history)
    db.commit()

    return email_history