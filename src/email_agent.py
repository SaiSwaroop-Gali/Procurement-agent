import os
from datetime import datetime

from dotenv import load_dotenv
from google import genai

from manager_agent import interpret_manager_instructions


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_purchase_order_email(
    request,
    manager_instructions
):

    ai_analysis = request.get(
        "ai_analysis",
        "No AI analysis available."
    )

    manager_decision = interpret_manager_instructions(

        request["recommended_order"],

        manager_instructions

    )

    final_quantity = manager_decision[
        "final_quantity"
    ]

    priority = manager_decision[
        "priority"
    ]

    reason = manager_decision[
        "reason"
    ]

    current_datetime = datetime.now().strftime(
        "%d %B %Y | %H:%M CET"
    )

    prompt = f"""
You are a professional airline procurement officer.

Generate a natural, human-like purchase order email.

Follow EXACTLY this writing style:

------------------------------------------------

Subject: Urgent Purchase Order Request – Engine Oil Pressure Switch

Dear XYZ Components Team,

I hope you are doing well.

We would like to place an urgent purchase order for the following component:

Part Name: Engine Oil Pressure Switch
Quantity: 10 units

Our stock for this item has dropped below the minimum operational level, and we require immediate replenishment to avoid any disruption in ongoing maintenance activities.

Kindly process this request at the highest priority and share an order confirmation along with the expected delivery date. Given the critical nature of this component, the earliest possible dispatch would be greatly appreciated.

Thank you for your prompt attention and support.

Warm regards,

AI Procurement System
Logistics & Supply Chain Department
Demo Airlines Ltd.
03 July 2026 | 17:30 CET

------------------------------------------------

Now generate a similar email using the following information:

Part Name:
{request["part_name"]}

Current Stock:
{request["current_stock"]}

Final Quantity:
{final_quantity}

Supplier:
{request["supplier_name"]}

AI Analysis:
{ai_analysis}

Manager Instructions:
{manager_instructions}

AI Manager Decision:
{reason}

Priority:
{priority}

Current Date and Time:
{current_datetime}

Rules:

1. Use the same tone and structure as the example.

2. Do NOT use markdown (** or bullets).

3. Start with:
I hope you are doing well.

4. If Priority is HIGH, use:

Urgent Purchase Order Request – <Part Name>

Otherwise use:

Purchase Order Request – <Part Name>

5. Respect the AI manager decision.

6. Mention the final quantity, not the original recommendation.

7. End with EXACTLY:

Warm regards,

AI Procurement System
Logistics & Supply Chain Department
Demo Airlines Ltd.

{current_datetime}

Return ONLY in this format:

SUBJECT:
...

BODY:
...
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        parts = text.split("BODY:")

        subject = (
            parts[0]
            .replace("SUBJECT:", "")
            .strip()
        )

        body = parts[1].strip()

        return {
            "subject": subject,
            "body": body
        }

    except Exception as e:

        print(f"Gemini Error: {e}")

        if priority == "HIGH":

            subject = (
                f"Urgent Purchase Order Request – "
                f"{request['part_name']}"
            )

            intro = (
                "We would like to place an urgent "
                "purchase order for the following "
                "component:"
            )

            priority_text = (
                "Kindly process this request at the "
                "highest priority and share an order "
                "confirmation along with the expected "
                "delivery date. Given the critical "
                "nature of this component, the earliest "
                "possible dispatch would be greatly "
                "appreciated."
            )

        else:

            subject = (
                f"Purchase Order Request – "
                f"{request['part_name']}"
            )

            intro = (
                "We would like to place a purchase "
                "order for the following component:"
            )

            priority_text = (
                "Kindly share an order confirmation "
                "along with the expected delivery date "
                "at your earliest convenience."
            )

        body = f"""
Dear {request['supplier_name']} Team,

I hope you are doing well.

{intro}

Part Name: {request['part_name']}
Quantity: {final_quantity} units

Our stock for this item has dropped below the minimum operational level, and we require immediate replenishment to avoid any disruption in ongoing maintenance activities.

{priority_text}

Thank you for your prompt attention and support.

Warm regards,

AI Procurement System
Logistics & Supply Chain Department
Demo Airlines Ltd.
{current_datetime}
"""

        return {
            "subject": subject,
            "body": body
        }