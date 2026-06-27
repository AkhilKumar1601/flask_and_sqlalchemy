import yfinance as yf


def get_stock_info(symbol):
    stock = yf.Ticker(symbol)

    info = stock.info

    return {
        "name": info.get("longName"),
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "sector": info.get("sector")
    }
