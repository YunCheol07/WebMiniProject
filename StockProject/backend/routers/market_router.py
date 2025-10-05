from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from urllib.parse import quote
import feedparser
import logging

from database import get_db, Stock
from services.korea_investment import ki_service

router = APIRouter(prefix="/api/stock", tags=["주식 시장 데이터"])
logger = logging.getLogger(__name__)


@router.get("/current/{stock_code}")
async def get_current_price(stock_code: str, db: Session = Depends(get_db)):
    """현재가 조회"""
    stock = db.query(Stock).filter(Stock.stock_code == stock_code).first()
    if not stock:
        raise HTTPException(status_code=404, detail="DB에 등록되지 않은 종목입니다")
    
    try:
        result = ki_service.get_current_price(stock_code)
        return result
    except Exception as e:
        logger.error(f"현재가 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chart/{stock_code}")
async def get_stock_chart(
    stock_code: str,
    period: str = Query("D"),
    db: Session = Depends(get_db)
):
    """차트 데이터 조회"""
    stock = db.query(Stock).filter(Stock.stock_code == stock_code).first()
    if not stock:
        raise HTTPException(status_code=404, detail="DB에 등록되지 않은 종목입니다")
    
    try:
        result = ki_service.get_stock_chart(stock_code, period)
        return result
    except Exception as e:
        logger.error(f"차트 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/news/{stock_code}")
async def get_stock_news(stock_code: str, db: Session = Depends(get_db)):
    """뉴스 조회"""
    stock = db.query(Stock).filter(Stock.stock_code == stock_code).first()
    stock_name = stock.stock_name if stock else f"종목{stock_code}"
    
    try:
        search_query = quote(stock_name)
        news_url = f"https://news.google.com/rss/search?q={search_query}+주식&hl=ko&gl=KR&ceid=KR:ko"
        
        feed = feedparser.parse(news_url)
        
        news_items = []
        for entry in feed.entries[:10]:
            news_items.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.get('published', ''),
                'source': entry.get('source', {}).get('title', 'Unknown')
            })
        
        return {
            "success": True,
            "stock_code": stock_code,
            "stock_name": stock_name,
            "news_count": len(news_items),
            "news": news_items
        }
    except Exception as e:
        logger.error(f"뉴스 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))
