# class Account

## attributes

account_url - api url

account_number

account_hash - used as the account number value for requests

## get_account_info()

### description

gets current account balances

### params

none

### returns

```
{
  'cashBalance': 3501.13,
  'availableFunds': 3501.13,
  'buyingPower': 7002.62,
  'dayTradingBuyingPower': 8002.0,
  'equity': 3501.13
}
```

## get_orders()

### description

gets account orders

### params

- maxResults: int = 100
- fromDate: str = None
  - yyyy-MM-dd'T'HH:mm:ss.SSSZ
  - 2024-03-29T00:00:00.000Z
  - \*requires toDate
- toDate: str = None
  - yyyy-MM-dd'T'HH:mm:ss.SSSZ
  - 2024-03-29T00:00:00.000Z
  - \*requires fromDate
- status: str = "WORKING"
  - [AWAITING_PARENT_ORDER, AWAITING_CONDITION, AWAITING_STOP_CONDITION, AWAITING_MANUAL_REVIEW, ACCEPTED, AWAITING_UR_OUT, PENDING_ACTIVATION, QUEUED, WORKING, REJECTED, PENDING_CANCEL, CANCELED, PENDING_REPLACE, REPLACED, FILLED, EXPIRED, NEW, AWAITING_RELEASE_TIME, PENDING_ACKNOWLEDGEMENT, PENDING_RECALL, UNKNOWN]

### returns

- [Order (see below)]

## place_orders()

### params

- Order (see below)

### returns

- order_id: int

## preview_order()

### description

preview an order to check validity

### params

- Order (see below)

### returns

- Order (see below)

## cancel_order()

### params

- OrderId: int

### returns

- success: boolean

## replace_order()

### description

replaces an existing order

### params

- OrderId (int)
- Order (see below)

### returns

- success: boolean

## format_order()

### description

assists in formatting order for the request

### params (see objects below for param options)

- symbol: str
- order_type: str
- quantity: int
- legs: list[dict]
  - Leg (see below)
- asset_type: str
- order_strategy_type: str
- order_id: Optional[int] = None
- stop_price: Optional[float] = None
- stop_price_linkBasis: Optional[str] = None
- stop_price_linkType: Optional[str] = None
- stop_price_offset: Optional[float] = None
- stop_type: Optional[str] = None
- price_link_basis: Optional[str] = None,
- price_link_type: Optional[str] = None,
- price: Optional[str] = None
- session="NORMAL"
- duration="DAY"
- complex_order_strategy_type="NONE"
- tax_lot_method="FIFO"
- position_effect="OPENING"
- specialInstruction: special_instruction

### returns

- Order (see below)

## format_leg()

### description

assists in formatting legs

### params

- leg_id: int,
- order_leg_type: str,
- instruction: str,
- asset_type: str,
- quantity: int,
- position_effect: str,
- symbol: Optional[str] = None,

### returns

- Leg (see below)

## <br>

<br>

## Order (object)

### Note

This is a simplified version of the full order payload available. See online docs.

### schema

- duration
  - [ DAY, GOOD_TILL_CANCEL, FILL_OR_KILL, IMMEDIATE_OR_CANCEL, END_OF_WEEK, END_OF_MONTH, NEXT_END_OF_MONTH ]
- orderType
  - [ MARKET, LIMIT, STOP, STOP_LIMIT, TRAILING_STOP, CABINET, NON_MARKETABLE, MARKET_ON_CLOSE, EXERCISE, TRAILING_STOP_LIMIT, NET_DEBIT, NET_CREDIT, NET_ZERO, LIMIT_ON_CLOSE ]
- complexOrderStrategyType
  - [ NONE, COVERED, VERTICAL, BACK_RATIO, CALENDAR, DIAGONAL, STRADDLE, STRANGLE, COLLAR_SYNTHETIC, BUTTERFLY, CONDOR, IRON_CONDOR, VERTICAL_ROLL, COLLAR_WITH_STOCK, DOUBLE_DIAGONAL, UNBALANCED_BUTTERFLY, UNBALANCED_CONDOR, UNBALANCED_IRON_CONDOR, UNBALANCED_VERTICAL_ROLL, MUTUAL_FUND_SWAP, CUSTOM ]
- quantity: int
- priceLinkBasis
  - [ MANUAL, BASE, TRIGGER, LAST, BID, ASK, ASK_BID, MARK, AVERAGE ]
- priceLinkType
  - [ VALUE, PERCENT, TICK ]
- price: float
- orderLegCollection: [Leg (see below)]
- taxLotMethod: tax_lot_method
- orderStrategyType: order_strategy_type
- stopPrice: float
- stopPriceLinkBasis
  - [ MANUAL, BASE, TRIGGER, LAST, BID, ASK, ASK_BID, MARK, AVERAGE ]
- stopPriceLinkType
  - [ VALUE, PERCENT, TICK ]
- stopPriceOffset: float
- stopType
  - [ STANDARD, BID, ASK, LAST, MARK ]
- session
  - [ NORMAL, AM, PM, SEAMLESS ]
- specialInstruction
  - [ ALL_OR_NONE, DO_NOT_REDUCE, ALL_OR_NONE_DO_NOT_REDUCE ]

## Leg (object)

### Note

This is a simplified version of the full order payload available. See online docs.

### schema

- orderLegType
  - [ EQUITY, OPTION, INDEX, MUTUAL_FUND, CASH_EQUIVALENT, FIXED_INCOME, CURRENCY, COLLECTIVE_INVESTMENT ]
  - instrument
    - symbol: str
    - assetType
      - [ EQUITY, OPTION, INDEX, MUTUAL_FUND, CASH_EQUIVALENT, FIXED_INCOME, CURRENCY, COLLECTIVE_INVESTMENT ]
- instruction
  - [ BUY, SELL, BUY_TO_COVER, SELL_SHORT, BUY_TO_OPEN, BUY_TO_CLOSE, SELL_TO_OPEN, SELL_TO_CLOSE, EXCHANGE, SELL_SHORT_EXEMPT ]
- positionEffect
  - [ OPENING, CLOSING, AUTOMATIC ]
- quantity: int
