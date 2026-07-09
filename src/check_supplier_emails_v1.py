import os
import imaplib
import email

from dotenv import load_dotenv

from src.supplier_response_agent import (
    analyze_supplier_email
)

from src.request_store import (
    get_request,
    update_supplier_response
)

from src.supplier_tool import (
    get_supplier_emails
)


load_dotenv()


EMAIL_ADDRESS = os.getenv(
    "EMAIL_ADDRESS"
)

EMAIL_APP_PASSWORD = os.getenv(
    "EMAIL_APP_PASSWORD"
)

IMAP_SERVER = os.getenv(
    "IMAP_SERVER",
    "imap.gmail.com"
)


def check_supplier_emails():

    print("\nChecking supplier emails...\n")

    valid_supplier_emails = get_supplier_emails()

    mail = imaplib.IMAP4_SSL(
        IMAP_SERVER
    )

    mail.login(
        EMAIL_ADDRESS,
        EMAIL_APP_PASSWORD
    )

    mail.select("inbox")

    # =====================================
    # UNREAD EMAILS ONLY
    # =====================================

    status, messages = mail.search(
        None,
        "UNSEEN"
    )

    email_ids = messages[0].split()

    print(
        f"Found {len(email_ids)} unread email(s)."
    )

    for email_id in email_ids:

        _, data = mail.fetch(
            email_id,
            "(RFC822)"
        )

        raw_email = data[0][1]

        msg = email.message_from_bytes(
            raw_email
        )

        sender = msg["From"]

        sender_email = sender.split("<")[-1] \
            .replace(">", "") \
            .strip() \
            .lower()

        subject = msg["Subject"]

        print("\n----------------")
        print(f"From: {sender_email}")
        print(f"Subject: {subject}")

        # =====================================
        # VALIDATE SUPPLIER
        # =====================================

        if sender_email not in valid_supplier_emails:

            print(
                f"Skipping non-supplier email: "
                f"{sender_email}"
            )

            continue

        # =====================================
        # EXTRACT EMAIL BODY
        # =====================================

        body = ""

        if msg.is_multipart():

            for part in msg.walk():

                if (
                    part.get_content_type()
                    == "text/plain"
                ):

                    body = part.get_payload(
                        decode=True
                    ).decode(
                        errors="ignore"
                    )

                    break

        else:

            body = msg.get_payload(
                decode=True
            ).decode(
                errors="ignore"
            )

        # =====================================
        # ANALYZE EMAIL
        # =====================================

        result = analyze_supplier_email(
            body
        )

        if result is None:

            print(
                "Could not analyze email."
            )

            continue

        request_id = result.get(
            "request_id"
        )

        if not request_id:

            print(
                "No request ID found. Skipping."
            )

            continue

        # =====================================
        # CHECK DATABASE
        # =====================================

        request = get_request(
            request_id
        )

        if request is None:

            print(
                f"Request {request_id} not found."
            )

            continue

        # =====================================
        # UPDATE DATABASE
        # =====================================

        update_supplier_response(

            request_id,

            result["supplier_status"],

            result["expected_delivery_date"],

            result["supplier_response"]

        )

        # =====================================
        # MARK EMAIL AS READ
        # =====================================

        mail.store(
            email_id,
            "+FLAGS",
            "\\Seen"
        )

        print(
            f"Updated request: {request_id}"
        )

    mail.logout()

    print(
        "\nSupplier email check completed.\n"
    )


if __name__ == "__main__":

    check_supplier_emails()