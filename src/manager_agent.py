import os
import json

from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def interpret_manager_instructions(
    original_quantity,
    instructions
):

    prompt = f"""
You are an airline procurement manager assistant.

Original recommended quantity:

{original_quantity}

Manager instructions:

{instructions}

Your task:

1. Determine the FINAL quantity.

Examples:

"add 10 more"
-> original + 10

"order 5 extra units"
-> original + 5

"double the quantity"
-> original * 2

"make it 25"
-> final = 25

"set quantity to 30"
-> final = 30

2. Determine priority:

HIGH:
urgent
asap
immediately
priority high
critical

NORMAL:
otherwise

Return ONLY valid JSON:

{{
    "final_quantity": 14,
    "priority": "HIGH",
    "reason": "Added 10 units and marked as urgent."
}}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return json.loads(
            response.text.strip()
        )

    except Exception as e:

        print(
            f"Manager Agent Error: {e}"
        )

        return {

            "final_quantity":
                original_quantity,

            "priority":
                "NORMAL",

            "reason":
                "AI interpretation failed."

        }