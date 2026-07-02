import asyncio

from inventory_tool import get_low_stock_items
from supplier_tool import get_supplier
from order_manager import recommend_order_quantity

from notification_tool import NotificationTool
from models import ProcurementRequest

from request_store import save_request
from database import init_db

from risk_utils import calculate_risk_level


class ProcurementAgent:

    def __init__(self):

        self.notification_tool = NotificationTool()

    def run(self):

        init_db()

        print("\n🤖 Procurement Agent Started\n")

        low_stock_items = get_low_stock_items()

        if low_stock_items.empty:

            print("✅ No items require reordering.")

            return

        asyncio.run(
            self.process_requests(
                low_stock_items
            )
        )

    async def process_requests(
        self,
        low_stock_items
    ):

        for _, item in low_stock_items.iterrows():

            supplier = get_supplier(
                item["supplier_id"]
            )

            order_quantity = recommend_order_quantity(
                item["current_stock"],
                item["reorder_threshold"]
            )

            # ==========================
            # BUSINESS RISK CALCULATION
            # ==========================

            risk_level = calculate_risk_level(

                item["part_name"],

                item["current_stock"],

                item["reorder_threshold"]

            )

            request = ProcurementRequest(

                part_id=item["part_id"],

                part_name=item["part_name"],

                current_stock=item["current_stock"],

                recommended_order=order_quantity,

                supplier_name=supplier["supplier_name"],

                supplier_email=supplier["email"],

                ai_analysis="Awaiting manager approval.",

                risk_level=risk_level,

                manager_instructions=""

            )

            save_request(request)

            self.display_request(request)

            try:

                await self.notification_tool.send_notification(
                    request
                )

                print(
                    f"✅ Notification sent for "
                    f"{request.part_name}"
                )

            except Exception as e:

                print(
                    f"❌ Telegram Error: {e}"
                )

    def display_request(
        self,
        request
    ):

        print(f"""
===================================

⚠️ PROCUREMENT ALERT

Request ID:
{request.request_id}

Part:
{request.part_name}

Part ID:
{request.part_id}

Current Stock:
{request.current_stock}

Recommended Order:
{request.recommended_order}

Supplier:
{request.supplier_name}

Supplier Email:
{request.supplier_email}

Risk Level:
{request.risk_level}

Status:
{request.status}

===================================
""")


if __name__ == "__main__":

    agent = ProcurementAgent()

    agent.run()