from pydantic import BaseModel
from typing import List


class StockResponse(BaseModel):
    stock_code: str
    stock_name: str


class StockSearchResponse(BaseModel):
    success: bool
    count: int
    query: str
    stocks: List[StockResponse]
