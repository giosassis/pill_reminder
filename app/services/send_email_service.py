import boto3
import logging
from app.config import ses_config
from app.database import SessionLocal
from app.models.email_history import EmailHistory
from app.utils.generate_history_id import generate_history_id
from datetime import datetime

ses_client = boto3.client(
    'ses',
    aws_access_key_id=ses_config.AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=ses_config.AWS_SECRET_ACCESS_KEY,  
    region_name=ses_config.AWS_REGION
)

def send_email(recipient, subject, body):
    """Função que envia e-mail através do AWS SES."""
    try:
        response = ses_client.send_email(
            Source=ses_config.SENDER_EMAIL,
            Destination={'ToAddresses': [recipient]},  
            Message={
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body,
                    },
                },
            }
        )
        db = SessionLocal() 
        email_log = EmailHistory(
            id=generate_history_id(),  
            recipient_email=recipient,
            status="Success",
            sent_at=datetime.utcnow(),
            subject=subject,
            error_message=None 
        )
        db.add(email_log)  
        db.commit()  
        db.close()  

        logging.info(f"Email was successfully sent to {recipient}")

        return response

    except Exception as e:
        db = SessionLocal() 
        email_log = EmailHistory(
            id=generate_history_id(),
            recipient_email=recipient,
            status="Failed",
            sent_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            subject=subject,
            error_message=str(e)  
        )
        db.add(email_log)  
        db.commit() 
        db.close() 

        logging.error(f"There was an error when trying to send email: {str(e)}")
        return None