import smtplib
import collections
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from config import SMTP_PORT, SMTP_SERVER, SENDER_EMAIL, RECEIVER_EMAIL, EMAIL_PASSWORD, TOP_ERROR_COUNT


def send_email(task_name, task, log_name, results):
    message = prepare_email(task_name, task, log_name, results)
    print("Sending notification.")
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        print("Notification sent.")
        

def prepare_email(task_name, task, log_name, results):
    message = MIMEMultipart()
    message["Subject"] = f'Report for DB modification task: {task_name}'
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    most_common_errors = collections.Counter(results['error']).most_common(TOP_ERROR_COUNT)
    error_text = ''
    if most_common_errors:
        error_text += f'Most common errors:'
        for error in most_common_errors:
            error_text += f'<p>{error[0]} - occurrences: {error[1]}</p>'

    text = f'<h2>Hi!</h2>' \
           f'<h3>Here are the results for you DB update task - {task_name}: {task}.</h2>' \
           f'<p>Successful operations: {results["success"]}</p>' \
           f'<p>Failed operations: {len(results["error"])}</p>' \
           f'{error_text}' \
           f'<br>' \
           f'<p>Enjoy your day</p>' \
           f'Postgres DB Updater'

    email_body = MIMEText(f'<html><b>{text}</b></html>', 'html')
    message.attach(email_body)

    with open(log_name) as log:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(log.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=log_name)
        encoders.encode_base64(attachment)

    message.attach(attachment)

    return message
