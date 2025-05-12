# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment variables (for this process)

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
EMAIL_ADDR = os.getenv("EMAIL_ADDR")
EMAIL_APP_PASS = os.getenv("EMAIL_APP_PASS")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT_TLS = os.getenv("SMTP_PORT_TLS")
DEBUG = os.getenv('DEBUG')
