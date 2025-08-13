import base64
import os
import time

import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

SCHW_KEY = os.getenv("SCHW_KEY")
SCHW_SECRET = os.getenv("SCHW_SECRET")


def refresh(refresh_token: str) -> dict:
    logger.info("Refreshing token...")

    refresh_token_value = refresh_token

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token_value,
    }
    headers = {
        "Authorization": f'Basic {base64.b64encode(f"{SCHW_KEY}:{SCHW_SECRET}".encode()).decode()}',
        "Content-Type": "application/x-www-form-urlencoded",
    }

    refresh_token_response = requests.post(
        url="https://api.schwabapi.com/v1/oauth/token",
        headers=headers,
        data=payload,
    )
    if refresh_token_response.status_code != 200:
        logger.error(f"Error refreshing access token: {refresh_token_response.text}")
        return None

    refresh_token_dict = refresh_token_response.json()

    logger.info("Refreshed token successfully.")

    return {
        "access_token": refresh_token_dict["access_token"],
        "refresh_token": refresh_token_dict["refresh_token"],
        "access_expires_at": int(time.time()) + int(refresh_token_dict["expires_in"]),
    }
