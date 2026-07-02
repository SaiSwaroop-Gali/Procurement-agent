import os
import smtplib

from email.mime.text import MIMEText
from dotenv import load_dotenv


load_dotenv()


EMAIL_ADDRESS = os.getenv(
    "EMAIL_ADDRESS"
)

EMAIL_APP_PASSWORD = os.getenv(
    "EMAIL_APP_PASSWORD"
)


def send_email(
    to_email,
    subject,
    body
):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    try:

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as server:

            server.login(
                EMAIL_ADDRESS,
                EMAIL_APP_PASSWORD
            )

            server.send_message(msg)

        print(
            f"✅ Email sent to {to_email}"
        )

    except Exception as e:

        print(
            f"❌ Email error: {e}"
        )