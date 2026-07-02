import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from request_store import (
    get_request,
    update_status
)

from user_state import (
    set_pending_modification,
    get_pending_modification,
    clear_pending_modification
)

from email_agent import generate_purchase_order_email
from gmail_tool import send_email


load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    action, request_id = query.data.split(":")

    request = get_request(request_id)

    if request is None:

        await query.edit_message_text(
            "❌ Request not found."
        )

        return

    # ==========================
    # APPROVE
    # ==========================

    if action == "approve":

        await query.edit_message_text(
            "🤖 Generating purchase order email..."
        )

        try:

            update_status(
                request_id,
                "APPROVED"
            )

            email_data = generate_purchase_order_email(
                request,
                manager_instructions=(
                    "No modifications. "
                    "Use original recommendation."
                )
            )

            send_email(
                request["supplier_email"],
                email_data["subject"],
                email_data["body"]
            )

            update_status(
                request_id,
                "EMAIL_SENT"
            )

            await query.message.reply_text(
                f"""
✅ Purchase Order Sent Successfully

Part:
{request["part_name"]}

Quantity:
{request["recommended_order"]}

Supplier:
{request["supplier_name"]}

Email:
{request["supplier_email"]}

Subject:
{email_data["subject"]}

Status:
EMAIL_SENT
"""
            )

            print("\n========================")
            print("STANDARD PURCHASE ORDER SENT")
            print("========================")

            print(f"Request ID: {request_id}")
            print(f"Part: {request['part_name']}")
            print(f"Supplier: {request['supplier_name']}")

            print("========================\n")

        except Exception as e:

            print(e)

            await query.message.reply_text(
                f"""
❌ Failed to send email

Error:

{str(e)}
"""
            )

    # ==========================
    # REJECT
    # ==========================

    elif action == "reject":

        update_status(
            request_id,
            "REJECTED"
        )

        await query.edit_message_text(
            f"""
❌ ORDER REJECTED

Part:
{request["part_name"]}

Status:
REJECTED
"""
        )

    # ==========================
    # MODIFY
    # ==========================

    elif action == "modify":

        update_status(
            request_id,
            "MODIFICATION_REQUESTED"
        )

        chat_id = query.message.chat_id

        set_pending_modification(
            chat_id,
            request_id
        )

        await query.edit_message_text(
            f"""
✏️ MODIFY REQUEST

Part:
{request["part_name"]}

Please send your modifications.

Examples:

• Order 15 instead of 10
• Mark as urgent
• Change supplier
"""
        )


async def handle_modification_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.message.chat_id

    request_id = get_pending_modification(
        chat_id
    )

    if request_id is None:

        return

    request = get_request(
        request_id
    )

    if request is None:

        await update.message.reply_text(
            "❌ Request not found."
        )

        return

    modification_text = update.message.text

    clear_pending_modification(
        chat_id
    )

    await update.message.reply_text(
        "🤖 Generating customized purchase order email..."
    )

    try:

        email_data = generate_purchase_order_email(
            request,
            modification_text
        )

        send_email(
            request["supplier_email"],
            email_data["subject"],
            email_data["body"]
        )

        update_status(
            request_id,
            "EMAIL_SENT"
        )

        await update.message.reply_text(
            f"""
✅ Customized Purchase Order Sent

Part:
{request["part_name"]}

Supplier:
{request["supplier_name"]}

Email:
{request["supplier_email"]}

Subject:
{email_data["subject"]}

Status:
EMAIL_SENT
"""
        )

        print("\n========================")
        print("CUSTOMIZED PURCHASE ORDER SENT")
        print("========================")

        print(f"Request ID: {request_id}")
        print(f"Part: {request['part_name']}")
        print(f"Supplier: {request['supplier_name']}")

        print("\nManager Instructions:")
        print(modification_text)

        print("========================\n")

    except Exception as e:

        print(e)

        await update.message.reply_text(
            f"""
❌ Failed to send email

Error:

{str(e)}
"""
        )


def main():

    app = Application.builder() \
        .token(BOT_TOKEN) \
        .build()

    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_modification_message
        )
    )

    print(
        "🤖 Telegram Listener Running..."
    )

    app.run_polling()


if __name__ == "__main__":

    main()