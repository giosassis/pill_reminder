import boto3
import logging
from app.config import ses_config

ses_client = boto3.client(
    'ses',
    aws_access_key_id=ses_config.AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=ses_config.AWS_SECRET_ACCESS_KEY,  
    region_name=ses_config.AWS_REGION 
)

def send_email(recipient_emails, subject, body):
    if not isinstance(recipient_emails, list):
        recipient_emails = [recipient_emails] 
    
    try:
        response = ses_client.send_email(
            Source=ses_config.SENDER_EMAIL,  
            Destination={'ToAddresses': recipient_emails}, 
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
        logging.info(f"Email was successfully sent to {recipient_emails}")
        return response
    except Exception as e:
        logging.error(f"Falha ao enviar e-mail: {str(e)}")
        return None
