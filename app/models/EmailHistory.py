from sqlalchemy import Column, String, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.models.Base import Base


class EmailHistory(Base):
    __tablename__ = "email_history"

    id = Column(String, primary_key=True, index=True)
    recipient_email = Column(String, nullable=False)
    status = Column(String, nullable=False)
    sent_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    subject = Column(String, nullable=False)
    error_message = Column(Text, nullable=True)
