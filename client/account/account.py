import os
from typing import Optional

from dotenv import load_dotenv

from utils.requests import delete, get, post, put

load_dotenv()


class Account:
    def __init__(self):
        self.account_url = os.getenv("ACCOUNT_URL")
        self.account_number = os.getenv("ACCOUNT_NUMBER")
        self.account_hash = os.getenv("ACCOUNT_HASH")  # use for account number

    def get_account_info(self):
        url = f"{self.account_url}/accounts/{self.account_hash}"
        response = get(url, auth=True)
        if response.ok:
            data = response.json()
            return {
                "cashBalance": data["securitiesAccount"]["currentBalances"][
                    "cashBalance"
                ],
                "availableFunds": data["securitiesAccount"]["currentBalances"][
                    "availableFunds"
                ],
                "buyingPower": data["securitiesAccount"]["currentBalances"][
                    "buyingPower"
                ],
                "dayTradingBuyingPower": data["securitiesAccount"]["currentBalances"][
                    "dayTradingBuyingPower"
                ],
                "equity": data["securitiesAccount"]["currentBalances"]["equity"],
            }
        else:
            raise Exception(response.text)

    def get_order(self, order_id: int) -> dict:
        url = f"{self.account_url}/accounts/{self.account_hash}/orders/{order_id}"
        response = get(url, auth=True)
        if response.ok:
            return response.json()
        else:
            raise Exception(response.text)

    def get_orders(
        self,
        maxResults: int = 100,
        fromDate: str = None,
        toDate: str = None,
        status: str = "WORKING",
    ):
        url = f"{self.account_url}/accounts/{self.account_hash}/orders"
        params = {
            "maxResults": maxResults,
            "fromEnteredTime": fromDate,
            "toEnteredTime": toDate,
            "status": status,
        }
        response = get(url, params=params, auth=True)
        if response.ok:
            return response.json()
        else:
            raise Exception(response.text)

    def place_order(self, order: dict) -> bool:
        url = f"{self.account_url}/accounts/{self.account_hash}/orders"
        response = post(url, data=order, auth=True)
        if response.ok:
            location = response.headers.get("Location", "")
            order_id = location.split("/")[-1] if location else None
            return order_id
        else:
            raise Exception(response.text)

    def preview_order(self, order: dict) -> bool:
        url = f"{self.account_url}/accounts/{self.account_hash}/previewOrder"
        response = post(url, data=order, auth=True)
        if response.ok:
            return response.json()
        else:
            raise Exception(response.text)

    def cancel_order(self, order_id: int) -> bool:
        url = f"{self.account_url}/accounts/{self.account_hash}/orders/{order_id}"
        response = delete(url, auth=True)
        if response.ok:
            return True
        else:
            raise Exception(response.text)

    def replace_order(self, order_id: int, order: dict) -> bool:
        url = f"{self.account_url}/accounts/{self.account_hash}/orders/{order_id}"
        response = put(url, data=order, auth=True)
        if response.ok:
            return True
        else:
            raise Exception(response.text)

    def format_order(
        symbol: str,
        order_type: str,
        quantity: int,
        legs: list[dict],
        order_strategy_type: str,
        stop_price: Optional[float] = None,
        stop_price_link_basis: Optional[str] = None,
        stop_price_link_type: Optional[str] = None,
        stop_price_offset: Optional[float] = None,
        stop_type: Optional[str] = None,
        price_link_basis: Optional[str] = None,
        price_link_type: Optional[str] = None,
        price: Optional[float] = None,
        session="NORMAL",
        duration="DAY",
        complex_order_strategy_type="NONE",
        tax_lot_method="FIFO",
        special_instruction: Optional[str] = None,
    ):

        post_order_payload = {
            "duration": duration,
            "orderType": order_type,
            "complexOrderStrategyType": complex_order_strategy_type,
            "quantity": quantity,
            "stopPrice": stop_price,
            "stopPriceLinkBasis": stop_price_link_basis,
            "stopPriceLinkType": stop_price_link_type,
            "stopPriceOffset": stop_price_offset,
            "stopType": stop_type,
            "priceLinkBasis": price_link_basis,
            "priceLinkType": price_link_type,
            "price": price,
            "orderLegCollection": legs,
            "taxLotMethod": tax_lot_method,
            "orderStrategyType": order_strategy_type,
            "session": session,
            "specialInstruction": special_instruction,
        }

        return post_order_payload

    def format_leg(
        order_leg_type: str,
        instruction: str,
        asset_type: str,
        quantity: int,
        position_effect: Optional[str] = "AUTOMATIC",
        symbol: Optional[str] = None,
    ):
        return {
            "orderLegType": order_leg_type,
            "instrument": {
                "symbol": symbol,
                "assetType": asset_type,
            },
            "instruction": instruction,
            "positionEffect": position_effect,
            "quantity": quantity,
        }
