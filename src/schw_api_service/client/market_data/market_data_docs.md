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

###

get historical candles

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

- frequencyType: str
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
