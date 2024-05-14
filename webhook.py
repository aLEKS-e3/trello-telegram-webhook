import os
import requests

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from database import write_user_to_db


load_dotenv()

CHAT_ID = None
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

app = FastAPI()
bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


class TelegramUpdate(BaseModel):
    update_id: int
    message: dict


def set_telegram_webhook(webhook: str) -> dict:
    webhook = webhook + "/telegram"
    url = TELEGRAM_API_URL + f"/setWebhook?url={webhook}"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )
    return response.json()


@app.head("/trello")
async def accept_trello_webhook() -> dict:
    return {"status": "ok"}


@app.post("/telegram")
async def telegram_webhook(update: TelegramUpdate) -> dict:
    global CHAT_ID

    CHAT_ID = update.message["chat"]["id"]
    name = update.message["from"]["first_name"]
    username = update.message["from"]["username"]
    await write_user_to_db(name, username)

    message = f"Hey, {name}"
    await bot.send_message(chat_id=CHAT_ID, text=message)

    return {"status": "ok"}


@app.post("/trello")
async def trello_webhook(request: Request) -> dict:
    payload = await request.json()

    if payload.get("action", {}).get("type") == "updateCard":
        data = payload["action"]["data"]

        card = data["card"]["name"]
        old_list = data["listBefore"]["name"]
        new_list = data["listAfter"]["name"]
        board = payload["model"]["name"]

        message = (
            f"Card '{card}' was moved from list '{old_list}' "
            f"to list '{new_list}' on board '{board}'"
        )
        await bot.send_message(chat_id=CHAT_ID, text=message)

    return {"status": "ok"}
