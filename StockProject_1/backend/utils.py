from datetime import datetime, timezone

def utc_now():
    """timezone-aware UTC 현재 시간 반환"""
    return datetime.now(timezone.utc)

def to_utc(dt: datetime) -> datetime:
    """timezone-naive datetime을 UTC로 변환"""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """datetime을 문자열로 포맷"""
    return dt.strftime(format_str)