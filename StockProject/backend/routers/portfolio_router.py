from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import logging

from database import get_db, Portfolio, Stock, User
from auth import get_current_user
from services.korea_investment import ki_service

router = APIRouter(prefix="/api/portfolio", tags=["포트폴리오"])
logger = logging.getLogger(__name__)


# Pydantic 스키마
class PortfolioAdd(BaseModel):
    stock_code: str
    quantity: int
    avg_price: int
    purchase_date: str  # YYYY-MM-DD 형식


class PortfolioUpdate(BaseModel):
    quantity: Optional[int] = None
    avg_price: Optional[int] = None


@router.get("")
async def get_portfolio(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    사용자의 포트폴리오 조회 (실시간 가격 포함)
    """
    try:
        portfolio_items = db.query(Portfolio)\
            .filter(Portfolio.user_id == current_user.user_id)\
            .order_by(Portfolio.created_at.desc())\
            .all()
        
        result = []
        total_purchase_amount = 0
        total_current_value = 0
        
        for item in portfolio_items:
            stock = item.stock
            
            # 실시간 현재가 조회
            try:
                current_price_data = ki_service.get_current_price(stock.stock_code)
                current_price = int(current_price_data['output']['stck_prpr'])
            except Exception as e:
                logger.error(f"현재가 조회 실패 ({stock.stock_code}): {e}")
                current_price = item.avg_price  # 실패 시 평균 매입가 사용
            
            # 계산
            purchase_amount = item.avg_price * item.quantity
            current_value = current_price * item.quantity
            profit_loss = current_value - purchase_amount
            profit_loss_rate = (profit_loss / purchase_amount * 100) if purchase_amount > 0 else 0
            
            total_purchase_amount += purchase_amount
            total_current_value += current_value
            
            result.append({
                "portfolio_id": item.portfolio_id,
                "stock_id": stock.stock_id,
                "stock_code": stock.stock_code,
                "stock_name": stock.stock_name,
                "quantity": item.quantity,
                "avg_price": item.avg_price,
                "current_price": current_price,
                "purchase_amount": purchase_amount,
                "current_value": current_value,
                "profit_loss": profit_loss,
                "profit_loss_rate": round(profit_loss_rate, 2),
                "purchase_date": item.purchase_date.isoformat(),
                "created_at": item.created_at.isoformat()
            })
        
        # 전체 손익
        total_profit_loss = total_current_value - total_purchase_amount
        total_profit_loss_rate = (total_profit_loss / total_purchase_amount * 100) if total_purchase_amount > 0 else 0
        
        return {
            "success": True,
            "count": len(result),
            "portfolio": result,
            "summary": {
                "total_purchase_amount": total_purchase_amount,
                "total_current_value": total_current_value,
                "total_profit_loss": total_profit_loss,
                "total_profit_loss_rate": round(total_profit_loss_rate, 2)
            }
        }
    
    except Exception as e:
        logger.error(f"포트폴리오 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def add_to_portfolio(
    portfolio_data: PortfolioAdd,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    포트폴리오에 주식 추가
    """
    try:
        # 종목 확인
        stock = db.query(Stock).filter(Stock.stock_code == portfolio_data.stock_code).first()
        if not stock:
            raise HTTPException(status_code=404, detail="종목을 찾을 수 없습니다")
        
        # 날짜 파싱
        try:
            purchase_date = datetime.strptime(portfolio_data.purchase_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="날짜 형식이 올바르지 않습니다 (YYYY-MM-DD)")
        
        # 이미 존재하는지 확인
        existing = db.query(Portfolio).filter(
            Portfolio.user_id == current_user.user_id,
            Portfolio.stock_id == stock.stock_id
        ).first()
        
        if existing:
            # 기존 항목 업데이트 (수량 평균화)
            total_quantity = existing.quantity + portfolio_data.quantity
            total_amount = (existing.avg_price * existing.quantity) + (portfolio_data.avg_price * portfolio_data.quantity)
            new_avg_price = total_amount // total_quantity
            
            existing.quantity = total_quantity
            existing.avg_price = new_avg_price
            
            db.commit()
            db.refresh(existing)
            
            return {
                "success": True,
                "message": "기존 보유 종목의 수량과 평균 매입가가 업데이트되었습니다",
                "portfolio_id": existing.portfolio_id
            }
        
        # 새로 추가
        new_portfolio = Portfolio(
            user_id=current_user.user_id,
            stock_id=stock.stock_id,
            quantity=portfolio_data.quantity,
            avg_price=portfolio_data.avg_price,
            purchase_date=purchase_date
        )
        
        db.add(new_portfolio)
        db.commit()
        db.refresh(new_portfolio)
        
        return {
            "success": True,
            "message": "포트폴리오에 추가되었습니다",
            "portfolio_id": new_portfolio.portfolio_id,
            "stock_code": stock.stock_code,
            "stock_name": stock.stock_name
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"포트폴리오 추가 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{portfolio_id}")
async def update_portfolio(
    portfolio_id: int,
    portfolio_data: PortfolioUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    포트폴리오 항목 수정
    """
    try:
        portfolio_item = db.query(Portfolio).filter(
            Portfolio.portfolio_id == portfolio_id,
            Portfolio.user_id == current_user.user_id
        ).first()
        
        if not portfolio_item:
            raise HTTPException(status_code=404, detail="포트폴리오 항목을 찾을 수 없습니다")
        
        if portfolio_data.quantity is not None:
            portfolio_item.quantity = portfolio_data.quantity
        
        if portfolio_data.avg_price is not None:
            portfolio_item.avg_price = portfolio_data.avg_price
        
        db.commit()
        db.refresh(portfolio_item)
        
        return {
            "success": True,
            "message": "포트폴리오가 수정되었습니다",
            "portfolio_id": portfolio_item.portfolio_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"포트폴리오 수정 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{portfolio_id}")
async def remove_from_portfolio(
    portfolio_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    포트폴리오에서 삭제
    """
    try:
        portfolio_item = db.query(Portfolio).filter(
            Portfolio.portfolio_id == portfolio_id,
            Portfolio.user_id == current_user.user_id
        ).first()
        
        if not portfolio_item:
            raise HTTPException(status_code=404, detail="포트폴리오 항목을 찾을 수 없습니다")
        
        stock = portfolio_item.stock
        
        db.delete(portfolio_item)
        db.commit()
        
        return {
            "success": True,
            "message": "포트폴리오에서 삭제되었습니다",
            "stock_code": stock.stock_code,
            "stock_name": stock.stock_name
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"포트폴리오 삭제 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))
