import yfinance as yf


def get_stock_info(symbol):
    stock = yf.Ticker(symbol)

    info = stock.info
    history = stock.history(period="1mo")

    one_month_return = None

    if len(history) > 1:
        first_price = history["Close"].iloc[0]
        last_price = history["Close"].iloc[-1]

        one_month_return = round(
            ((last_price - first_price) / first_price) * 100,
            2
        )

    return {
        "name": info.get("longName"),
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "sector": info.get("sector"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
        "volume": info.get("volume"),
        "average_volume": info.get("averageVolume"),
        "one_month_return_percent": one_month_return
    }
