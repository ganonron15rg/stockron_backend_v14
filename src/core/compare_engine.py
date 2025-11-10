import asyncio
from src.providers.yahoo_agent import YahooAgent

async def compare_tickers(tickers: list[str]):
    yahoo = YahooAgent()
    results = []
    for t in tickers:
        try:
            data = yahoo.fetch(t)
            results.append({"ticker": t, "data": data})
        except Exception as e:
            results.append({"ticker": t, "error": str(e)})
    return {"compare": results}
