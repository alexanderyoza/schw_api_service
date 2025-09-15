import asyncio
import json
import os
from datetime import datetime

import websockets
from dotenv import load_dotenv
from loguru import logger

from ...auth.token_service import get_access_token
from ...utils.requests import get

load_dotenv()


class MarketData:
    def __init__(self):
        self.market_data_url = os.getenv("MARKET_DATA_URL")
        self.account_url = os.getenv("ACCOUNT_URL")

    def get_quote(self, symbol: str, fields=None) -> dict:
        url = f"{self.market_data_url}/{symbol}/quotes"
        params = {
            "fields": fields,
        }
        response = get(url, params=params, auth=True)
        if response.ok:
            return response.json()
        else:
            raise Exception(response.text)

    def get_quotes(self, symbols: str, fields=None, indicative=False) -> dict:
        url = f"{self.market_data_url}/quotes"
        params = {
            "symbols": symbols,
            "fields": fields,
            "indicative": indicative,
        }
        response = get(url, params=params, auth=True)
        if response.ok:
            return response.json()
        else:
            raise Exception(response.text)

    def get_historical_prices(
        self,
        symbol: str,
        period: int,
        period_type: str,
        frequency: int,
        frequency_type: str,
        start_date: datetime = None,
        end_date: datetime = None,
        need_extended_hours_data: bool = False,
        need_previous_close: bool = False,
    ) -> dict:
        url = f"{self.market_data_url}/pricehistory"
        params = {
            "symbol": symbol,
            "period": period,
            "periodType": period_type,
            "frequency": frequency,
            "frequencyType": frequency_type,
            "startDate": int(start_date.timestamp() * 1000) if start_date else None,
            "endDate": int(end_date.timestamp() * 1000) if end_date else None,
            "needExtendedHoursData": need_extended_hours_data,
            "needPreviousClose": need_previous_close,
        }
        response = get(url, params=params, auth=True)
        if response.ok:
            return response.json()
        else:
            raise Exception(response.text)

    async def init_stream_prices(self, callback, service, symbols, fields):
        preferences = self._get_preferences()
        self.socket_url = preferences["streamerInfo"][0]["streamerSocketUrl"]
        self.client_id = preferences["streamerInfo"][0]["schwabClientCustomerId"]
        self.client_correl_id = preferences["streamerInfo"][0]["schwabClientCorrelId"]
        self.client_channel = preferences["streamerInfo"][0]["schwabClientChannel"]
        self.client_function_id = preferences["streamerInfo"][0][
            "schwabClientFunctionId"
        ]
        self.callback = callback
        self.service = service
        self.symbols = symbols
        self.fields = fields
        token = get_access_token()
        login_msg = {
            "requests": [
                {
                    "requestid": 1,
                    "service": "ADMIN",
                    "command": "LOGIN",
                    "SchwabClientCustomerId": self.client_id,
                    "SchwabClientCorrelId": self.client_correl_id,
                    "parameters": {
                        "Authorization": token,
                        "SchwabClientChannel": self.client_channel,
                        "SchwabClientFunctionId": self.client_function_id,
                    },
                }
            ]
        }
        self.ws = await websockets.connect(self.socket_url)
        await self.ws.send(json.dumps(login_msg))
        logger.info("Waiting for login response...")
        for _ in range(10):
            try:
                message = await asyncio.wait_for(self.ws.recv(), timeout=5)
                msg_json = json.loads(message)
                if (
                    msg_json["response"]
                    and msg_json["response"][0]["command"] == "LOGIN"
                    and msg_json["response"][0]["content"]["code"] == 0
                ):
                    break
                await asyncio.sleep(0.5)
            except Exception as e:
                logger.error(e)
            except asyncio.TimeoutError:
                logger.error("No login message received within timeout.")

        logger.info("Logged in")

    async def subscribe_to_prices(self):
        level_one_msg = {
            "requests": [
                {
                    "service": self.service,
                    "requestid": 2,
                    "command": "SUBS",
                    "SchwabClientCustomerId": self.client_id,
                    "SchwabClientCorrelId": self.client_correl_id,
                    "parameters": {
                        "keys": self.symbols,
                        "fields": self.fields,
                    },
                }
            ]
        }
        await self.ws.send(json.dumps(level_one_msg))
        logger.info("Waiting for subscription response...")
        async for message in self.ws:
            msg_json = json.loads(message)
            if not msg_json or "notify" in msg_json:
                continue
            try:
                if (
                    "response" in msg_json
                    and msg_json["response"][0]["command"] == "SUBS"
                    and msg_json["response"][0]["content"]["code"] == 0
                ):
                    break
            except Exception as e:
                logger.error(e)

        logger.info(f"Subscribed to {self.symbols} with fields {self.fields}")

        async for message in self.ws:
            msg_json = json.loads(message)
            if not msg_json or "notify" in msg_json:
                continue
            await self.callback(msg_json)

    async def close_stream_prices(self):
        unsub = {
            "requests": [
                {
                    "requestid": 3,
                    "service": "ADMIN",
                    "command": "LOGOUT",
                    "SchwabClientCustomerId": self.client_id,
                    "SchwabClientCorrelId": self.client_correl_id,
                    "parameters": {},
                }
            ]
        }
        await self.ws.send(json.dumps(unsub))
        # wait for logout response
        logger.info("Waiting for logout response...")
        for _ in range(10):
            try:
                message = await asyncio.wait_for(self.ws.recv(), timeout=5)
                msg_json = json.loads(message)
                if (
                    "response" in msg_json
                    and msg_json["response"][0]["command"] == "LOGOUT"
                    and msg_json["response"][0]["content"]["code"] == 0
                ):
                    break
                await asyncio.sleep(0.5)
            except asyncio.TimeoutError:
                logger.error("No message within timeout.")
        logger.info("Logged out")
        await self.ws.close()

    def _get_preferences(self):
        url = f"{self.account_url}/userPreference"
        response = get(url, auth=True)
        if response.ok:
            return response.json()
        else:
            raise Exception(response.text)


"""
<< {"response":[{"service":"ADMIN","command":"LOGIN","requestid":"1","SchwabClientCorrelId":"60b4c643-ca26-d965-1d21-ad96078ab2fa","timestamp":1755118704102,"content":{"code":0,"msg":"server=s3081dc7-2;status=NP"}}]}
<< {"notify":[{"heartbeat":"1755118704127"}]}
<< {"response":[{"service":"LEVELONE_EQUITIES","command":"SUBS","requestid":"3","SchwabClientCorrelId":"60b4c643-ca26-d965-1d21-ad96078ab2fa","timestamp":1755118704127,"content":{"code":0,"msg":"SUBS command succeeded"}}]}
<< {"data":[{"service":"LEVELONE_EQUITIES", "timestamp":1755118704147,"command":"SUBS","content":[{"key":"AAPL","delayed":false,"assetMainType":"EQUITY","assetSubType":"COE","cusip":"037833100","1":233.22,"2":233.33,"3":233.3,"4":1,"5":3,"8":69783235,"10":235}]}]}
<< {"data":[{"service":"LEVELONE_EQUITIES", "timestamp":1755118706289,"command":"SUBS","content":[{"key":"AAPL","3":233.31,"8":69783236}]}]}
<< {"data":[{"service":"LEVELONE_EQUITIES", "timestamp":1755118712559,"command":"SUBS","content":[{"key":"AAPL","1":233.33,"2":233.39,"3":233.34,"5":1,"8":69784498}]}]}
<< {"data":[{"service":"LEVELONE_EQUITIES", "timestamp":1755118714580,"command":"SUBS","content":[{"key":"AAPL","3":233.35,"8":69784508}]}]}
<< {"data":[{"service":"LEVELONE_EQUITIES", "timestamp":1755118715590,"command":"SUBS","content":[{"key":"AAPL","3":233.36,"8":69784619}]}]}
<< {"data":[{"service":"LEVELONE_EQUITIES", "timestamp":1755118716611,"command":"SUBS","content":[{"key":"AAPL","8":69784645}]}]}
"""
