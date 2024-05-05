import smtplib
import requests

from config import rules
from local_config import MAILGUN_APIKEY

from email.mime.text import MIMEText


def send_api_email(subject, body):
    return requests.post(
        "https://api.mailgun.net/v3/inprobes/messages",
        auth=("api", MAILGUN_APIKEY),
        data={
            "from": "Hosein finance@inprobes.com",
            "to": ["hs.ramezanpoor@gmail.com", "hosein@inprobes.com"],
            "subject": subject,
            "text": body
        }
    )


def send_smtp_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = ""
    msg['To'] = rules['send_email']['email_receiver']

    try:
        with smtplib.SMTP('', 25) as mail_server:
            mail_server.starttls()  # Enable TLS if required
            mail_server.login('', MAILGUN_APIKEY)
            mail_server.sendmail(msg['From'], msg['To'], msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)
