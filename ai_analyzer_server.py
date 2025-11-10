# =============================================================
# 🧠 Stockron AI Analyzer v14.0
# FastAPI server - Modular multi-agent analysis system
# =============================================================
from fastapi import FastAPI, HTTPException
from src.models.requests import AnalyzeRequest, CompareRequest
from src.providers.yahoo_agent import YahooAgent
from src.providers.alpha_agent import AlphaAgent
from src.providers.finnhub_agent import FinnhubAgent
from src.core.scoring import compute_scores, stance_from_overall
from src.core.news_engine import fetch_news
from src.core.compare_engine import compare_tickers
from datetime import datetime

app = FastAPI(title="Stockron Analyzer v14")

def iso():
    return datetime.utcnow().isoformat() + "Z"


@app.get("/")
async def home():
    return {"status": "ok", "version": "v14.0"}


@app.get("/health")
async def health():
    return {"ok": True, "time": iso()}


@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    ticker = req.ticker.upper().strip()
    try:
        yahoo = YahooAgent()
        base_data = yahoo.fetch(ticker)
    except Exception as e:
        try:
            alpha = AlphaAgent()
            base_data = alpha.fetch(ticker)
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Data fetch failed: {ex}")

    raw = base_data.get("raw_quote", {})
    pe = raw.get("pe", 0)
    eps = raw.get("eps_growth", 0)
    rev = raw.get("rev_growth", 0)
    rsi = 55  # placeholder for technical score

    scores = compute_scores(pe, eps, rev, rsi)
    stance = stance_from_overall(scores["overall_score"])

    return {
        "ticker": ticker,
        "scores": scores,
        "ai_stance": stance,
        "source": base_data.get("source", "YahooAgent"),
        "timestamp": iso(),
    }


@app.get("/news/{ticker}")
async def news(ticker: str):
    data = await fetch_news(ticker)
    return {"ticker": ticker, "news": data}


@app.post("/compare")
async def compare(req: CompareRequest):
    return await compare_tickers(req.tickers)
