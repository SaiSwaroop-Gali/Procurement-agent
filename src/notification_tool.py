import os

from dotenv import load_dotenv
from telegram import (
    Bot,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


load_dotenv()


class NotificationTool:

    def __init__(self):

        self.bot_token = os.getenv(
            "TELEGRAM_BOT_TOKEN"
        )

        self.chat_id = os.getenv(
            "TELEGRAM_CHAT_ID"
        )

        self.bot = Bot(
            token=self.bot_token
        )

    def build_keyboard(self, request):

        keyboard = [

            [
                InlineKeyboardButton(
                    "✅ Approve",
                    callback_data=f"approve:{request.request_id}"
                ),

                InlineKeyboardButton(
                    "❌ Reject",
                    callback_data=f"reject:{request.request_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    "✏️ Modify",
                    callback_data=f"modify:{request.request_id}"
                )
            ]
        ]

        return InlineKeyboardMarkup(keyboard)

    def format_message(self, request):

        risk_emoji = {

            "HIGH": "🔴",

            "MEDIUM": "🟡",

            "LOW": "🟢"

        }

        risk_display = (
            f"{risk_emoji.get(request.risk_level, '⚪')} "
            f"{request.risk_level}"
        )

        return f"""
⚠️ PROCUREMENT REQUEST

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

Risk Category:
{risk_display}

Supplier:
{request.supplier_name}

Choose an action:
"""

    async def send_notification(self, request):

        keyboard = self.build_keyboard(request)

        await self.bot.send_message(
            chat_id=self.chat_id,
            text=self.format_message(request),
            reply_markup=keyboard
        )