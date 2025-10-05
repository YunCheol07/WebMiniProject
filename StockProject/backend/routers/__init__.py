from .auth_router import router as auth_router
from .stock_router import router as stock_router
from .watchlist_router import router as watchlist_router
from .market_router import router as market_router

__all__ = [
    "auth_router",
    "stock_router",
    "watchlist_router",
    "market_router"
]
