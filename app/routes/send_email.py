from fastapi import APIRouter
from app.services.send_email_service import send_email
from pydantic import BaseModel
from typing import List
from fastapi import BackgroundTasks
from datetime import datetime

# Definindo o APIRouter
router = APIRouter()

class EmailRequest(BaseModel):
    subject: str
    recipients: List[str]
    body: str

@router.post("/send_email/")
async def send_email_endpoint(email: EmailRequest, background_tasks: BackgroundTasks):
    for recipient in email.recipients:
        background_tasks.add_task(send_email, recipient, email.subject, email.body)
        return {"message": f"Email was successfully sent to {recipient} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
