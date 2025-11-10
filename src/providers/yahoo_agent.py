import yfinance as yf

class YahooAgent:
    def fetch(self, ticker: str):
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "raw_quote": {
                "symbol": ticker.upper(),
                "price": float(info.get("currentPrice", 0)),
                "pe": float(info.get("trailingPE", 0)),
                "market_cap": float(info.get("marketCap", 0)),
                "eps_growth": float(info.get("earningsQuarterlyGrowth", 0) or 0),
                "rev_growth": float(info.get("revenueGrowth", 0) or 0),
            },
            "source": "YahooAgent"
        }
