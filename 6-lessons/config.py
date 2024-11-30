from dotenv import load_dotenv
import os

load_dotenv()

token = os.environ.get('token')
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")