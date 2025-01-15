import boto3
import logging
from datetime import datetime
from sqlalchemy import func
from jinja2 import Environment, FileSystemLoader
from app.config import ses_config, settings
from app.database import SessionLocal
from app.models.EmailHistory import EmailHistory
from app.utils.generate_history_id import generate_history_id
from app.repositories.medication_repository import MedicationRepository


email_template = Environment(
    loader=FileSystemLoader('app/utils/email_templates/'))

ses_client = boto3.client(
    'ses',
    aws_access_key_id=ses_config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=ses_config.AWS_SECRET_ACCESS_KEY,
    region_name=ses_config.AWS_REGION
)


def generate_email_context(medications):
    context = {
        "user_name": settings.USER_NAME,
        "medication": medications,
    }
    return context


def render_email_template(template_name, context):
    template = email_template.get_template(template_name)
    return template.render(context)


def send_email(recipient, subject, template_name):
    """Função que envia o e-mail com base nas informações do banco de dados."""

    db = SessionLocal()

    medications = MedicationRepository.get_medication_by_time(
        db, [datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

    if not medications:
        db.close()
        return "No medications scheduled for today."

    context = {
        "user_name": settings.USER_NAME,  # Ajuste para pegar do banco ou configuração
        "medications": [{"name": med.name, "schedule_times": med.schedule_times} for med in medications]
    }

    body = render_email_template(template_name, context)

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
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': body,
                    },
                },
            }
        )

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

        return response

    except Exception as e:
        db.close()
        logging.error(f"Erro ao enviar e-mail para {recipient}: {str(e)}")
        return None
