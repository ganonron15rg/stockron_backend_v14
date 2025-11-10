import os, httpx

class FinnhubAgent:
    def __init__(self):
        self.api_key = os.getenv("FINNHUB_API_KEY", "")
        self.base = "https://finnhub.io/api/v1"

    def fetch(self, ticker: str):
        if not self.api_key:
            raise RuntimeError("Finnhub API key missing")
        url = f"{self.base}/quote?symbol={ticker}&token={self.api_key}"
        r = httpx.get(url, timeout=8.0)
        data = r.json()
        if "c" not in data:
            raise RuntimeError("Invalid Finnhub response")
        return {
            "raw_quote": {
                "symbol": ticker,
                "price": data.get("c"),
                "high": data.get("h"),
                "low": data.get("l")
            },
            "source": "Finnhub"
        }
