import asyncio
import os

from dotenv import load_dotenv

from database import create_table
from trello import create_board, create_trello_columns, set_trello_webhook
from webhook import set_telegram_webhook, app

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK")


def set_telegram_up(webhook_url: str) -> None:
    set_telegram_webhook(webhook_url)


def set_trello_up(webhook_url: str) -> None:
    board_id = create_board("Board")
    create_trello_columns(board_id, ["Done", "InProgress"])
    set_trello_webhook(webhook_url, board_id)


if __name__ == "__main__":
    asyncio.run(create_table())
    set_telegram_up(WEBHOOK_URL)
    set_trello_up(WEBHOOK_URL)
