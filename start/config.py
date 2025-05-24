from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env file

# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = ["slot","card","equipment"]


# SQL Server
SQL_SERVER_URI = os.getenv("SQL_SERVER_URI")

# Email Alerts
ALERT_EMAIL = os.getenv("ALERT_EMAIL")
ALERT_PASSWORD = os.getenv("ALERT_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
