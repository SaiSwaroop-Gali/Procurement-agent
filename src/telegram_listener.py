# =====================================
# telegram_listener.py
# TEST VERSION
# Manager confirms raw message BEFORE AI processes it
# =====================================

import os

from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from request_store import (
    get_request,
    update_status,
    update_manager_instructions,
    update_ordered_quantity
)

from user_state import (
    set_pending_modification,
    get_pending_modification,
    set_pending_confirmation,
    get_pending_confirmation,
    clear_pending_modification
)

from email_tool import (
    generate_purchase_order_email
)

from gmail_tool import send_email


load_dotenv()

BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)


# =====================================
# EMAIL HELPER
# =====================================

async def send_customized_email(
    request,
    instructions,
    message
):

    print(f"DEBUG: send_customized_email called for {request['request_id']} with instructions='{instructions}'")

    try:

        email_data = generate_purchase_order_email(
            request,
            instructions
        )
        
        print(f"DEBUG: email_data generated: subject='{email_data['subject']}'")

        send_email(
            request["supplier_email"],
            email_data["subject"],
            email_data["body"]
        )

        update_ordered_quantity(
            request["request_id"],
            email_data["final_quantity"]
        )

        update_manager_instructions(
            request["request_id"],
            instructions
        )

        update_status(
            request["request_id"],
            "EMAIL_SENT"
        )

        await message.reply_text(
            f"""
✅ Purchase Order Sent Successfully

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
        print("PURCHASE ORDER SENT")
        print("========================")

        print(f"Request ID: {request['request_id']}")
        print(f"Part: {request['part_name']}")
        print(f"Supplier: {request['supplier_name']}")

        print("\nManager Instructions:")
        print(instructions)

        print("========================\n")

    except Exception as e:

        print(f"DEBUG: EXCEPTION in send_customized_email: {e}")

        import traceback
        traceback.print_exc()

        await message.reply_text(
            f"""
❌ Failed to send email

Error:

{str(e)}
"""
        )


# =====================================
# BUTTON HANDLER
# =====================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    action, request_id = query.data.split(":")

    print(f"DEBUG: button_handler triggered - action='{action}', request_id='{request_id}'")

    request = get_request(request_id)

    if request is None:

        print(f"DEBUG: request {request_id} not found in store")

        await query.edit_message_text(
            "❌ Request not found."
        )

        return


    # =====================================
    # APPROVE
    # =====================================

    if action == "approve":

        update_status(
            request_id,
            "APPROVED"
        )

        await query.edit_message_text(
            "🤖 Generating purchase order email..."
        )

        await send_customized_email(
            request,
            "No modifications. Use original recommendation.",
            query.message
        )


    # =====================================
    # REJECT
    # =====================================

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


    # =====================================
    # MODIFY
    # =====================================

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

        print(f"DEBUG: pending_modification set for chat_id={chat_id}, request_id={request_id}")

        await query.edit_message_text(
            f"""
✏️ MODIFY REQUEST

Part:
{request["part_name"]}

Please send your modifications.

Examples:

- Add 10 more units
- Double the quantity
- Set quantity to 25
- Make it urgent
"""
        )


    # =====================================
    # CONFIRM MODIFICATION
    # =====================================

    elif action == "confirm_modify":

        print(f"DEBUG: confirm_modify triggered for chat_id={query.message.chat_id}, request_id={request_id}")

        state = get_pending_confirmation(
            query.message.chat_id
        )

        print(f"DEBUG: pending_confirmation state = {state}")

        if state is None:

            print("DEBUG: state is None -> no pending confirmation found")

            await query.edit_message_text(
                "❌ No pending confirmation found."
            )

            return

        instructions = state["instructions"]

        print(f"DEBUG: instructions from state = '{instructions}'")

        update_manager_instructions(
            request_id,
            instructions
        )

        clear_pending_modification(
            query.message.chat_id
        )

        await query.edit_message_text(
            "🤖 Generating customized purchase order email..."
        )

        await send_customized_email(
            request,
            instructions,
            query.message
        )


    # =====================================
    # CANCEL
    # =====================================

    elif action == "cancel_modify":

        clear_pending_modification(
            query.message.chat_id
        )

        update_status(
            request_id,
            "PENDING_APPROVAL"
        )

        await query.edit_message_text(
            f"""
❌ Modification Cancelled

Part:
{request["part_name"]}

Status:
PENDING_APPROVAL
"""
        )


    # =====================================
    # MODIFY AGAIN
    # =====================================

    elif action == "modify_again":

        set_pending_modification(
            query.message.chat_id,
            request_id
        )

        print(f"DEBUG: modify_again -> pending_modification reset for chat_id={query.message.chat_id}, request_id={request_id}")

        await query.edit_message_text(
            f"""
✏️ MODIFY AGAIN

Part:
{request["part_name"]}

Please enter new instructions.

Examples:

- Add 10 more units
- Double the quantity
- Set quantity to 25
- Make it urgent
"""
        )


# =====================================
# MODIFICATION MESSAGE HANDLER
# =====================================

async def handle_modification_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.message.chat_id

    request_id = get_pending_modification(
        chat_id
    )

    print(f"DEBUG: handle_modification_message - chat_id={chat_id}, pending request_id={request_id}")

    if request_id is None:

        print("DEBUG: no pending modification -> ignoring message")

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

    print(f"DEBUG: modification_text received = '{modification_text}'")


    # =====================================
    # STORE FOR CONFIRMATION
    # =====================================

    set_pending_confirmation(

        chat_id,

        request_id,

        modification_text
    )

    print(f"DEBUG: pending_confirmation set for chat_id={chat_id}")


    keyboard = [

        [

            InlineKeyboardButton(
                "✅ Confirm",
                callback_data=f"confirm_modify:{request_id}"
            )

        ],

        [

            InlineKeyboardButton(
                "❌ Cancel",
                callback_data=f"cancel_modify:{request_id}"
            ),

            InlineKeyboardButton(
                "✏️ Modify Again",
                callback_data=f"modify_again:{request_id}"
            )

        ]
    ]


    markup = InlineKeyboardMarkup(
        keyboard
    )


    await update.message.reply_text(
        f"""
⚠️ PLEASE CONFIRM YOUR MODIFICATION

Part:
{request["part_name"]}

Your Instructions:

{modification_text}

Click Confirm to proceed.
""",
        reply_markup=markup
    )


# =====================================
# MAIN
# =====================================

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