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

@router.get("/market-news")
async def get_market_news(limit: int = Query(10, le=30)):
    """코스피 시장 뉴스 조회"""
    try:
        search_query = quote("코스피 주식시장")
        news_url = f"https://news.google.com/rss/search?q={search_query}&hl=ko&gl=KR&ceid=KR:ko"
        
        feed = feedparser.parse(news_url)
        
        news_items = []
        for entry in feed.entries[:limit]:
            news_items.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.get('published', ''),
                'source': entry.get('source', {}).get('title', 'Unknown')
            })
        
        return {
            "success": True,
            "count": len(news_items),
            "news": news_items
        }
    except Exception as e:
        logger.error(f"시장 뉴스 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top-stocks")
async def get_top_stocks(
    limit: int = Query(20, le=50),
    db: Session = Depends(get_db)
):
    """
    코스피 시가총액 상위 종목 조회 (2025년 10월 기준)
    """
    try:
        # 2025년 10월 코스피 시가총액 상위 종목 코드 (정확한 순서)
        top_stock_codes = [
            '005930',  # 1. 삼성전자
            '000660',  # 2. SK하이닉스
            '373220',  # 3. LG에너지솔루션
            '207940',  # 4. 삼성바이오로직스
            '005935',  # 5. 삼성전자우
            '012450',  # 6. 한화에어로스페이스
            '329180',  # 7. HD현대중공업
            '005380',  # 8. 현대차
            '105560',  # 9. KB금융
            '034020',  # 10. 두산에너빌리티
            '000270',  # 11. 기아
            '068270',  # 12. 셀트리온
            '035420',  # 13. NAVER
            '055550',  # 14. 신한지주
            '042660',  # 15. 한화오션
            '028260',  # 16. 삼성물산
            '032830',  # 17. 삼성생명
            '402340',  # 18. SK스퀘어
            '009540',  # 19. HD한국조선해양
            '012330',  # 20. 현대모비스
            '035720',  # 21. 카카오
            '086790',  # 22. 하나금융지주
            '015760',  # 23. 한국전력공사
            '005490',  # 24. POSCO홀딩스
            '051910',  # 25. LG화학
            '267260',  # 26. HD현대일렉트릭
            '011200',  # 27. HMM
            '287410',  # 28. 메리츠금융지주
            '066570',  # 29. LG전자
            '096770',  # 30. SK이노베이션
        ][:limit + 10]
        
        stocks_with_cap = []
        
        for stock_code in top_stock_codes:
            try:
                # DB에서 종목 정보 조회
                stock = db.query(Stock).filter(Stock.stock_code == stock_code).first()
                if not stock:
                    logger.warning(f"DB에 없는 종목: {stock_code}")
                    continue
                
                # 실시간 현재가 및 시가총액 조회
                stock_info = ki_service.get_stock_info(stock_code)
                
                stocks_with_cap.append({
                    "stock_code": stock.stock_code,
                    "stock_name": stock.stock_name,
                    "current_price": stock_info['current_price'],
                    "change": stock_info['change'],
                    "change_rate": stock_info['change_rate'],
                    "volume": stock_info['volume'],
                    "market_cap": stock_info['market_cap']
                })
                
            except Exception as e:
                logger.error(f"종목 조회 실패 ({stock_code}): {e}")
                continue
        
        # 실제 시가총액 기준 내림차순 정렬
        stocks_with_cap.sort(key=lambda x: x['market_cap'], reverse=True)
        
        # 상위 N개만 선택
        top_stocks = stocks_with_cap[:limit]
        
        # 순위 및 포맷팅 추가
        result = []
        for idx, stock in enumerate(top_stocks):
            result.append({
                "rank": idx + 1,
                "stock_code": stock['stock_code'],
                "stock_name": stock['stock_name'],
                "current_price": stock['current_price'],
                "change": stock['change'],
                "change_rate": stock['change_rate'],
                "volume": stock['volume'],
                "market_cap": stock['market_cap'],
                "market_cap_formatted": format_market_cap(stock['market_cap'])
            })
        
        return {
            "success": True,
            "count": len(result),
            "stocks": result
        }
        
    except Exception as e:
        logger.error(f"상위 종목 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def format_market_cap(market_cap: int) -> str:
    """시가총액을 읽기 쉽게 포맷팅"""
    if market_cap >= 1_000_000_000_000:
        return f"{market_cap / 1_000_000_000_000:.1f}조원"
    elif market_cap >= 100_000_000:
        return f"{market_cap / 100_000_000:.0f}억원"
    else:
        return f"{market_cap:,}원"