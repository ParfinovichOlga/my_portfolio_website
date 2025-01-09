import smtplib
from celery import shared_task
import os
from dotenv import load_dotenv

load_dotenv()
user_email = os.getenv("user_email")
user_password = os.getenv("user_password")

@shared_task
def send_email_task(message):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=user_email, password=user_password)
        connection.sendmail(from_addr=user_email, to_addrs=user_email, msg=message)