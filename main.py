import json
from datetime import datetime
from zoneinfo import ZoneInfo

from schw_api_service import SchwApiService


def main():
    schw_api_service = SchwApiService()

    data = schw_api_service.market_data.get_quote(
        symbol="AAPL",
        fields="quote,fundamental",
    )

    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
