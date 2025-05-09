# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env into environment variables (for this process)

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
