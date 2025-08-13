from .auth.token_service import get_access_token
from .client import Account, MarketData


class SchwApiService:
    def __init__(self, env: str = "prod"):
        self.access_token = get_access_token()
        self.account = Account()
        self.market_data = MarketData()


__all__ = [
    "SchwApiService",
    "Account",
    "MarketData",
    "get_access_token",
]
