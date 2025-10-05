from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import logging

from database import get_db, Watchlist, Stock, User
from auth import get_current_user

router = APIRouter(prefix="/api/watchlist", tags=["관심 종목"])
logger = logging.getLogger(__name__)


@router.get("")
async def get_watchlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """관심 종목 목록 조회"""
    watchlist_items = db.query(Watchlist)\
        .filter(Watchlist.user_id == current_user.user_id)\
        .order_by(Watchlist.added_at.desc())\
        .all()
    
    result = []
    for item in watchlist_items:
        stock = item.stock
        result.append({
            "watchlist_id": item.watchlist_id,
            "stock_id": stock.stock_id,
            "stock_code": stock.stock_code,
            "stock_name": stock.stock_name,
            "added_at": item.added_at.isoformat(),
            "alert_enabled": item.alert_enabled,
            "target_price": item.target_price
        })
    
    return {
        "success": True,
        "count": len(result),
        "watchlist": result
    }


@router.post("/{stock_code}")
async def add_to_watchlist(
    stock_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """관심 종목 추가"""
    stock = db.query(Stock).filter(Stock.stock_code == stock_code).first()
    if not stock:
        raise HTTPException(status_code=404, detail="종목을 찾을 수 없습니다")
    
    existing = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.user_id,
        Watchlist.stock_id == stock.stock_id
    ).first()
    
    if existing:
        return {
            "success": False,
            "message": "이미 관심 종목에 추가되어 있습니다",
            "watchlist_id": existing.watchlist_id
        }
    
    new_watchlist = Watchlist(
        user_id=current_user.user_id,
        stock_id=stock.stock_id,
        alert_enabled=False
    )
    
    db.add(new_watchlist)
    db.commit()
    db.refresh(new_watchlist)
    
    return {
        "success": True,
        "message": "관심 종목에 추가되었습니다",
        "watchlist_id": new_watchlist.watchlist_id,
        "stock_code": stock.stock_code,
        "stock_name": stock.stock_name
    }


@router.delete("/{stock_code}")
async def remove_from_watchlist(
    stock_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """관심 종목 삭제"""
    stock = db.query(Stock).filter(Stock.stock_code == stock_code).first()
    if not stock:
        raise HTTPException(status_code=404, detail="종목을 찾을 수 없습니다")
    
    watchlist_item = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.user_id,
        Watchlist.stock_id == stock.stock_id
    ).first()
    
    if not watchlist_item:
        return {
            "success": False,
            "message": "관심 종목에 없습니다"
        }
    
    db.delete(watchlist_item)
    db.commit()
    
    return {
        "success": True,
        "message": "관심 종목에서 삭제되었습니다",
        "stock_code": stock.stock_code,
        "stock_name": stock.stock_name
    }


@router.get("/check/{stock_code}")
async def check_in_watchlist(
    stock_code: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """관심 종목 포함 여부 확인"""
    stock = db.query(Stock).filter(Stock.stock_code == stock_code).first()
    if not stock:
        return {"in_watchlist": False}
    
    exists = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.user_id,
        Watchlist.stock_id == stock.stock_id
    ).first()
    
    return {
        "in_watchlist": exists is not None,
        "watchlist_id": exists.watchlist_id if exists else None
    }
