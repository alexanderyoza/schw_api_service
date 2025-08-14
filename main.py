import asyncio
import json
from asyncio import CancelledError

from schw_api_service import SchwApiService


async def stream_callback(message):
    print(json.dumps(message, indent=4))


async def main():
    try:
        schw_api_service = SchwApiService()
        try:
            await schw_api_service.market_data.init_stream_prices(
                callback=stream_callback,
                service="LEVELONE_EQUITIES",
                symbols="AAPL",
                fields="0,1,2,3,4,5,8,10,11",
            )
            await schw_api_service.market_data.subscribe_to_prices()
        except KeyboardInterrupt:
            print("🛑 Interrupted by user.")
        except asyncio.CancelledError:
            print("🛑 Cancelled by user.")
        except Exception as e:
            print("❌ Other error", e)
        finally:
            await schw_api_service.market_data.close_stream_prices()
            print("👋 Closed stream prices")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())
