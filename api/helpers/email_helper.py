from smtplib import SMTP
from email.mime.text import MIMEText
from core.config import EMAIL_ADDR, EMAIL_APP_PASS, SMTP_SERVER, SMTP_PORT_TLS


def send_email(usr_address: str):
    # TODO: This is a RickRoll, I'll have to add an actual URL when this is deployed
    messageText = "Click on the following link to confirm your email and activate your account: https://rb.gy/tosbcy"
    message = MIMEText(messageText)
    message["Subject"] = "Activate your account"
    message["From"] = EMAIL_ADDR
    message["To"] = usr_address  # Use TEST_EMAIL from .env (core.config) if necessary

    with SMTP(SMTP_SERVER, SMTP_PORT_TLS) as server:
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDR, EMAIL_APP_PASS)
        server.sendmail(EMAIL_ADDR, usr_address, message.as_string())
