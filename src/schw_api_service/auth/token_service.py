# pip install cryptography python-dotenv filelock
import base64
import json
import os
import secrets
import tempfile
import time
from pathlib import Path

import requests
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from filelock import FileLock
from loguru import logger

from .authorize import authorize
from .refresh_token import refresh

STORE_PATH = Path(".secrets/tokens.enc.json")
LOCK_PATH = str(STORE_PATH) + ".lock"
STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
load_dotenv()

SCHW_KEY = os.getenv("SCHW_KEY")
SCHW_SECRET = os.getenv("SCHW_SECRET")


def _fernet():
    key_material = os.environ["TOKEN_FILE_KEY"]
    k = base64.urlsafe_b64encode((key_material.encode() * 32)[:32])
    return Fernet(k)


def _load():
    if not STORE_PATH.exists():
        return None
    f = _fernet()
    data = json.loads(f.decrypt(STORE_PATH.read_bytes()).decode())
    return data


def _save(data: dict):
    f = _fernet()
    ct = f.encrypt(json.dumps(data).encode())
    with tempfile.NamedTemporaryFile(delete=False, dir=str(STORE_PATH.parent)) as tmp:
        tmp.write(ct)
        tempname = tmp.name
    os.replace(tempname, STORE_PATH)


def get_access_token(buffer_seconds: int = 60) -> str:
    with FileLock(LOCK_PATH, timeout=20):
        data = _load() or {}
        now = int(time.time())
        if not data or data.get("access_expires_at", 0) <= now + buffer_seconds:
            if "refresh_token" in data:
                data = refresh(data["refresh_token"])
            else:
                data = None

            if not data:
                logger.info("Token refresh failed. Attempting to re-authorize.")
                data = authorize()

            if not data:
                raise RuntimeError("Re-authorize attempt failed.")

            _save(data)
        return data["access_token"]
