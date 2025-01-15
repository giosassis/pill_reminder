from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import List
from app.services.send_email_service import send_email
import datetime 
router = APIRouter()

class EmailRequest(BaseModel):
    subject: str
    recipient: str
    template_name: str

@router.post("/send_email/")
async def send_email_endpoint(email: EmailRequest, background_tasks: BackgroundTasks):
    for recipient in email.recipient:
        background_tasks.add_task(send_email, recipient, email.subject, "reminder_email.html")
        return {"message": f"Emails were successfully sent to {len(email.recipient)} recipients at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}