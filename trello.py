import os
import requests

from requests import RequestException
from dotenv import load_dotenv


load_dotenv()

API = os.getenv("TRELLO_API")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK")


def get_query(name: str) -> dict:
    return {
        "name": name,
        "key": API,
        "token": TRELLO_TOKEN
    }


def create_board(name: str) -> str:
    url = "https://api.trello.com/1/boards/"
    query = get_query(name)

    response = requests.request(
        "POST",
        url,
        params=query
    )

    return response.json()["id"]


def create_trello_columns(board_id: str, names: list[str]) -> None:
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    headers = {
      "Accept": "application/json"
    }

    for name in names:
        query = get_query(name)

        requests.request(
           "POST",
           url,
           headers=headers,
           params=query
        )


def set_trello_webhook(webhook: str, board_id: str) -> None:
    response = requests.request(
        "POST",
        f"https://api.trello.com/1/tokens/{TRELLO_TOKEN}/webhooks/",
        params={
            "key": API,
            "idModel": board_id,
            "callbackURL": webhook + "/trello",
            "description": "Webhook"
        }
    )

    if response.status_code != 200:
        raise RequestException(f"Failed to register webhook: {response.text}")
