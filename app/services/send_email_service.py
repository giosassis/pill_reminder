import boto3
import logging
from app.config import ses_config  # Usando o ses_config para acessar as variáveis do SES

# Criação do cliente SES usando boto3
ses_client = boto3.client(
    'ses',
    aws_access_key_id=ses_config.AWS_ACCESS_KEY_ID,  # Usando o ses_config corretamente
    aws_secret_access_key=ses_config.AWS_SECRET_ACCESS_KEY,  # Usando o ses_config corretamente
    region_name=ses_config.AWS_REGION  # Usando o ses_config corretamente
)

def send_email(recipient_emails, subject, body):
    """
    Envia e-mails utilizando o AWS SES e registra os detalhes do envio.

    :param recipient_emails: Uma lista de endereços de e-mail dos destinatários.
    :param subject: O assunto do e-mail.
    :param body: O corpo do e-mail.
    :return: Resposta do SES ou None em caso de erro.
    """
    if not isinstance(recipient_emails, list):
        recipient_emails = [recipient_emails]  # Garante que o parâmetro seja uma lista
    
    try:
        # Logando todos os detalhes do envio do e-mail
        logging.info(f"Enviando e-mail com os seguintes dados:")
        logging.info(f"Remetente: {ses_config.SENDER_EMAIL}")
        logging.info(f"Destinatários: {', '.join(recipient_emails)}")
        logging.info(f"Assunto: {subject}")
        logging.info(f"Corpo do e-mail: {body}")

        # Envio do e-mail usando o AWS SES
        response = ses_client.send_email(
            Source=ses_config.SENDER_EMAIL,  # Usando o ses_config para acessar o remetente
            Destination={'ToAddresses': recipient_emails},  # Lista de destinatários
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

        # Logando a resposta do SES
        logging.info(f"Resposta do SES: {response}")

        return response
    except Exception as e:
        logging.error(f"Falha ao enviar e-mail: {str(e)}")
        return None
