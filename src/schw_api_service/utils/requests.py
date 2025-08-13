import json as _json

import requests

from ..auth.token_service import get_access_token


def get(url, params=None, auth=False):
    headers = {}
    if auth:
        access_token = get_access_token()
        headers["Authorization"] = f"Bearer {access_token}"

    response = requests.get(url, headers=headers, params=params)
    return response


def post(url, data=None, auth=False):
    headers = {
        "Content-Type": "application/json",
    }

    if auth:
        access_token = get_access_token()
        headers["Authorization"] = f"Bearer {access_token}"

    json_payload = data if isinstance(data, (dict, list)) else None
    response = requests.post(
        url,
        headers=headers,
        json=json_payload,
        data=None if json_payload is not None else data,
    )
    return response


def delete(url, data=None, auth=False):
    headers = {
        "Content-Type": "application/json",
    }

    if auth:
        access_token = get_access_token()
        headers["Authorization"] = f"Bearer {access_token}"

    json_payload = data if isinstance(data, (dict, list)) else None
    response = requests.delete(
        url,
        headers=headers,
        json=json_payload,
        data=None if json_payload is not None else data,
    )
    return response


def put(url, data=None, auth=False):
    headers = {
        "Content-Type": "application/json",
    }

    if auth:
        access_token = get_access_token()
        headers["Authorization"] = f"Bearer {access_token}"

    json_payload = data if isinstance(data, (dict, list)) else None
    response = requests.put(
        url,
        headers=headers,
        json=json_payload,
        data=None if json_payload is not None else data,
    )
    return response
