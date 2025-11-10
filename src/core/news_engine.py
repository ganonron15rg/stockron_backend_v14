import httpx, asyncio

async def fetch_news(ticker: str):
    urls = [
        f"https://news.google.com/rss/search?q={ticker}+stock",
        f"https://finance.yahoo.com/quote/{ticker}/news"
    ]
    results = []
    async with httpx.AsyncClient(timeout=10.0) as client:
        for url in urls:
            try:
                r = await client.get(url)
                results.append({"source": url, "status": r.status_code})
            except Exception as e:
                results.append({"source": url, "error": str(e)})
    return results
