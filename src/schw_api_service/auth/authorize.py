import base64
import os
import time
import webbrowser

import requests
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

SCHW_KEY = os.getenv("SCHW_KEY")
SCHW_SECRET = os.getenv("SCHW_SECRET")


def construct_init_auth_url() -> str:

    auth_url = f"https://api.schwabapi.com/v1/oauth/authorize?client_id={SCHW_KEY}&redirect_uri=https://127.0.0.1"

    logger.info("Click to authenticate:")
    logger.info(auth_url)

    return auth_url


def construct_headers_and_payload(returned_url):
    response_code = (
        f"{returned_url[returned_url.index('code=') + 5: returned_url.index('%40')]}@"
    )

    credentials = f"{SCHW_KEY}:{SCHW_SECRET}"
    base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Basic {base64_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    payload = {
        "grant_type": "authorization_code",
        "code": response_code,
        "redirect_uri": "https://127.0.0.1",
    }

    return headers, payload


def retrieve_tokens(headers, payload) -> dict:
    init_token_response = requests.post(
        url="https://api.schwabapi.com/v1/oauth/token",
        headers=headers,
        data=payload,
    )

    init_tokens_dict = init_token_response.json()

    return init_tokens_dict


def authorize() -> dict:
    cs_auth_url = construct_init_auth_url()
    webbrowser.open(cs_auth_url)

    logger.info("Paste Returned URL:")
    returned_url = input()

    init_token_headers, init_token_payload = construct_headers_and_payload(returned_url)

    init_tokens_dict = retrieve_tokens(
        headers=init_token_headers, payload=init_token_payload
    )

    logger.info("Authorization successful")

    return {
        "access_token": init_tokens_dict["access_token"],
        "refresh_token": init_tokens_dict["refresh_token"],
        "access_expires_at": int(time.time()) + int(init_tokens_dict["expires_in"]),
    }
