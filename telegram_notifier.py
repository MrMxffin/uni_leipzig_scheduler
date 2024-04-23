# telegram_notifier.py

import asyncio
from aiogram import Bot


class TelegramNotifier:
    """Notifier for sending messages via Telegram."""

    def __init__(self, token, chat_id):
        """Initialize the TelegramNotifier."""
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    async def send_message(self, message):
        """Send message asynchronously."""
        await self.bot.send_message(chat_id=self.chat_id, text=message)

    def notify(self, message):
        """Notify with the provided message."""
        asyncio.run(self.send_message(message))
