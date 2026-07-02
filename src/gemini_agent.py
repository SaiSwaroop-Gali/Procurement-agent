import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def procurement_reasoning(
    item,
    supplier_name,
    order_quantity
):

    prompt = f"""
You are an airline procurement expert.

Analyze:

Part:
{item['part_name']}

Current Stock:
{item['current_stock']}

Threshold:
{item['reorder_threshold']}

Recommended Order:
{order_quantity}

Supplier:
{supplier_name}

Provide:

1. Risk Level
2. Business Explanation
3. Final Recommendation

Keep it short.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text