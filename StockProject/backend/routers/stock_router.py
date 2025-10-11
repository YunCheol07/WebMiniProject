from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, case
from typing import List

from database import get_db, Stock

router = APIRouter(prefix="/api/stocks", tags=["주식 검색"])

@router.get("/list")  # 구체적인 경로를 먼저 등록
async def list_stocks(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """전체 종목 목록 조회"""
    query = db.query(Stock)
    total = query.count()
    stocks = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "success": True,
        "total": total,
        "page": page,
        "limit": limit,
        "stocks": [
            {
                "stock_code": stock.stock_code,
                "stock_name": stock.stock_name
            }
            for stock in stocks
        ]
    }

@router.get("/search")
async def search_stocks(
    q: str = Query(..., min_length=1, description="검색어"),
    limit: int = Query(10, le=50, description="결과 개수"),
    db: Session = Depends(get_db)
):
    """주식 종목 검색"""
    search_query = q.strip()
    
    priority = case(
        (Stock.stock_name.like(f"{search_query}%"), 1),
        (Stock.stock_code.like(f"{search_query}%"), 2),
        (Stock.stock_name.like(f"%{search_query}%"), 3),
        (Stock.stock_code.like(f"%{search_query}%"), 4),
        else_=5
    )
    
    conditions = or_(
        Stock.stock_name.like(f"%{search_query}%"),
        Stock.stock_code.like(f"%{search_query}%")
    )
    
    results = db.query(Stock)\
        .filter(conditions)\
        .order_by(priority, Stock.stock_name)\
        .limit(limit)\
        .all()
    
    return {
        "success": True,
        "count": len(results),
        "query": search_query,
        "stocks": [
            {
                "stock_code": stock.stock_code,
                "stock_name": stock.stock_name
            }
            for stock in results
        ]
    }


@router.get("/{stock_code}")
async def get_stock_info(stock_code: str, db: Session = Depends(get_db)):
    """특정 종목 정보 조회"""
    stock = db.query(Stock).filter(Stock.stock_code == stock_code).first()
    
    if not stock:
        raise HTTPException(status_code=404, detail="종목을 찾을 수 없습니다")
    
    return {
        "stock_code": stock.stock_code,
        "stock_name": stock.stock_name
    }
