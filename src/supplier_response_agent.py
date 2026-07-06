import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_supplier_email(email_text):

    prompt = f"""
You are an AI procurement assistant.

Analyze the supplier response email below.

Email:

{email_text}


Extract the following:

1. request_id

Example:
4c129736


2. supplier_status

Allowed values:

ACCEPTED
REJECTED
PARTIALLY_ACCEPTED
PENDING


3. expected_delivery_date

Return in YYYY-MM-DD format.

Return null if unavailable.


4. supplier_response

Give a short business summary.


Examples:

Example 1:

Email:

We confirm order 4c129736.

Expected delivery date:
15 July 2026.

Output:

{{
    "request_id": "4c129736",
    "supplier_status": "ACCEPTED",
    "expected_delivery_date": "2026-07-15",
    "supplier_response": "Supplier confirmed the order."
}}


Example 2:

Email:

Order 4c129736 cannot be fulfilled due to inventory shortage.

Output:

{{
    "request_id": "4c129736",
    "supplier_status": "REJECTED",
    "expected_delivery_date": null,
    "supplier_response": "Supplier rejected the order due to stock shortage."
}}


Return ONLY valid JSON.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        print("\n===== GEMINI RESPONSE =====")
        print(text)
        print("===========================\n")

        # Remove markdown code blocks if Gemini adds them
        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        return json.loads(
            text.strip()
        )

    except Exception as e:

        print(
            f"Supplier Response Agent Error: {e}"
        )

        return None