from pydantic import BaseModel
from typing import List

class AnalyzeRequest(BaseModel):
    ticker: str

class CompareRequest(BaseModel):
    tickers: List[str]
