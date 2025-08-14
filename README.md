# Charles Schwab API Service

# 👀 At a glance

Easily manage authentication, account information, and market data requests with the Charles Schwab API. This service does not provide comprehensive coverage of all capabilities that [Charles Schwab's Developer Portal](https://developer.schwab.com/) offers but rather is meant to help with getting started quickly on testing, trading, and analyzing stock market strategies.

# 💯 Motivation

This service is meant to be a lightweight, easy to use solution to easily access account and market data without needing to build a setup from scratch each time. It includes the areas that are most necessary to me when experimenting, researching, or learning about the stock market without needing to spend too much time sorting through large requests and responses.

# 🚀 Quick Start

### 1. Charles Schwab Developer Account Setup

1. [Create an account](https://developer.schwab.com/) to request access to the API here: https://developer.schwab.com/
2. Create you app in the dashboard and add both account and data access to the app.
3. Set the callback URL to https://127.0.0.1

### 2. ENV Setup

```
SCHW_KEY=<Charles Schwab API Key>
SCHW_SECRET=<Charles Schwab API Secret>

TOKEN_FILE_KEY=<generate with {python -c "import secrets; print(secrets.token_urlsafe(48))"}>

ACCOUNT_URL="https://api.schwabapi.com/trader/v1"
MARKET_DATA_URL="https://api/schwabapi.com/marketdata/v1"
ACCOUNT_NUMBER=<Account Number (GET with https://api.schwabapi.com/trader/v1/accounts/accountNumbers)>
ACCOUNT_HASH=<Account Hash (GET with https://api.schwabapi.com/trader/v1/accounts/accountNumbers)>
```

### 3. Using the service

#### 1. Initialize the SchwApiService to begin auth

```
  schw_api_service = SchwApiService()
```

#### 2. If you need to login to get a refresh token

- Login using your PORTFOLIO ACCOUNT information, not your developer login.
- Accept the terms and link your preferred account
  - Note: this script is currently only setup to manage one account at a time
- You should be directed to a not found page
  - Copy the url from the page you are on into the terminal url prompt
- Your tokens should be ready for service usage

#### More info

- Read docs in client/account and client/market_data
- Read through [Charles Schwab API Developer Documentation](https://developer.schwab.com/products)

### Coming soon...

- Get options price data

### References:

- [Charles Schwab API Developer Portal](https://developer.schwab.com/products)
- [tylerbowers - github repo](https://github.com/tylerebowers/Schwabdev/tree/main)
- [tylerbowers - youtube](https://www.youtube.com/@tylerebowers)
- [Reddit - r/Schwab](https://www.reddit.com/r/Schwab/comments/1c2ioe1/the_unofficial_guide_to_charles_schwabs_trader/?share_id=ilOFlRkDUXpFi-vE1ceBt&utm_content=2&utm_medium=ios_app&utm_name=ioscss&utm_source=share&utm_term=1)
