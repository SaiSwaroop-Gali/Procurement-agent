import os
from datetime import datetime

from dotenv import load_dotenv

from manager_agent import (
    interpret_manager_instructions
)


load_dotenv()


def generate_purchase_order_email(
    request,
    manager_instructions
):

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

    current_datetime = datetime.now().strftime(
        "%d %B %Y | %H:%M CET"
    )

    print("\n========== EMAIL DEBUG ==========")
    print(f"Request ID: {request['request_id']}")
    print(f"Original Recommended Order: {request['recommended_order']}")
    print(f"Manager Instructions: {manager_instructions}")
    print(f"Manager Decision: {manager_decision}")
    print("=================================\n")


    # =====================================
    # SUBJECT
    # =====================================

    if priority == "HIGH":

        subject = (
            f"Urgent Purchase Order Request "
            f"[{request['request_id']}] – "
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
            f"Purchase Order Request "
            f"[{request['request_id']}] – "
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


    # =====================================
    # EMAIL BODY
    # =====================================

    body = f"""
Dear {request['supplier_name']} Team,

I hope you are doing well.

{intro}

Purchase Order ID: {request['request_id']}

Part Name: {request['part_name']}
Quantity: {final_quantity} units

Our stock for this item has dropped below the minimum operational level, and we require immediate replenishment to avoid any disruption in ongoing maintenance activities.

{priority_text}

Please reference Purchase Order ID {request['request_id']} in all future communications and delivery documentation.

Thank you for your prompt attention and support.

Warm regards,

AI Procurement System
Logistics & Supply Chain Department
Demo Airlines Ltd.

{current_datetime}
"""

    return {
        "subject": subject,
        "body": body,
        "final_quantity": final_quantity
    }