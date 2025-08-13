from auth import get_access_token
from client import Account, MarketData


class SchwApiService:
    def __init__(self, env="prod"):
        self.access_token = get_access_token()
        self.account = Account()
        self.market_data = MarketData()
