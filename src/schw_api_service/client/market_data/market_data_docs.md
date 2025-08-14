# class MarketData

## attributes

market_data_url - api url

## get_quote()

### params

- symbol: str
  - 'ticker'
  - 'aapl'
- fields: str
  - 'field,field,field'
  - 'quote,fundamental'
  - [quote, fundamental, extended, reference, regular]
- indicative: boolean

### returns

- See online docs

## get

## get_quotes()

### params

- symbols: str
  - 'ticker,ticker'
  - 'aapl, msft'
  - None means get all
- fields: str
  - 'field,field,field'
  - 'quote,fundamental'
  - [quote, fundamental, extended, reference, regular]
- indicative: boolean

### returns

- See online docs

## get_historical_prices()

### params

- symbol: str
- period: int

  - (valid values based on periodType)
  - day: [1, 2, 3, 4, 5, 10]
  - month: [1, 2, 3, 6]
  - year: [1, 2, 3, 5, 10, 15, 20]
  - ytd: [1]

- periodType: str

  - [day, month, year, ytd]

- frequency: str

  - (valid values based on periodType)
  - day: [minute]
  - month: [daily, weekly]
  - year: [daily, weekly, monthly]
  - ytd: [daily, weekly]

- frequencyType: int
  - (valid values based on frequencyType)
  - minute: [1, 5, 10, 15, 30]
  - daily: [1]
  - weekly: [1]
  - monthly: [1]
- startDate: datetime
  - datetime(2025, 8, 12, 14, 30, 0, tzinfo=timezone.utc)
  - Converted to time in milliseconds since the UNIX epoch
- endDate: datetime
  - datetime(2025, 8, 12, 14, 30, 0, tzinfo=timezone.utc)
  - Converts to time in milliseconds since the UNIX epoch
- need_extended_hours_data=False
- need_previous_close=False

## returns

- See online docs

## init_stream_prices()

### description

Initializes class values for websocket streaming

### params

- callback: function
  - param: message: dict
- service: str
  - [LEVELONE_EQUITIES, LEVELONE_OPTIONS, LEVELONE_FUTURES, LEVELONE_FUTURES_OPTIONS, LEVELONE_FOREX, NYSE_BOOK, NASDAQ_BOOK, OPTIONS_BOOK, CHART_EQUITY, CHART_FUTURES, SCREENER_EQUITY, SCREENER_OPTION]
- symbols: str
  - 'ticker,ticker,ticker'
  - 'aapl,msft'
- fields: str
  - '1,2,4,5'
  - See online docs or codes in client/market_data file

### returns

none

## subscribe_to_prices()

### description

Subscribes to the prices given in init_stream_prices() and streams them to the callback function

### params

none

### returns

none

## close_stream_prices()

### description

Logs out of subscription

### params

none

### returns

none
