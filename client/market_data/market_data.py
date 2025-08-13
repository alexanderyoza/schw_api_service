import os
from datetime import datetime

from dotenv import load_dotenv

from utils.requests import get, post

load_dotenv()


class MarketData:
    def __init__(self):
        self.market_data_url = os.getenv("MARKET_DATA_URL")

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
        frequency: str,
        frequency_type: str,
        start_date: datetime,
        end_date: datetime,
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
            "startDate": int(start_date.timestamp() * 1000),
            "endDate": int(end_date.timestamp() * 1000),
            "needExtendedHoursData": need_extended_hours_data,
            "needPreviousClose": need_previous_close,
        }
        response = get(url, params=params, auth=True)
        if response.ok:
            return response.json()
        else:
            raise Exception(response.text)
