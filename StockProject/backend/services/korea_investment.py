import requests
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class KoreaInvestmentService:
    """한국투자증권 OpenAPI 서비스"""
    
    def __init__(self):
        self.access_token: Optional[str] = None
        self.config = {
            'REAL_APP_KEY': settings.REAL_APP_KEY,
            'REAL_APP_SECRET': settings.REAL_APP_SECRET,
            'REAL_URL': settings.REAL_URL,
            'REAL_CANO': settings.REAL_CANO,
            'REAL_ACNT_PRDT_CD': settings.REAL_ACNT_PRDT_CD
        }
    
    def get_access_token(self) -> Optional[str]:
        """토큰 발급"""
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.config['REAL_APP_KEY'],
            "appsecret": self.config['REAL_APP_SECRET']
        }
        
        PATH = "oauth2/tokenP"
        URL = f"{self.config['REAL_URL']}/{PATH}"
        
        try:
            logger.info(f"🔑 토큰 발급 시도: {URL}")
            res = requests.post(URL, headers=headers, data=json.dumps(body), timeout=10)
            
            if res.status_code == 200:
                self.access_token = res.json()["access_token"]
                logger.info("✅ 토큰 발급 성공")
                return self.access_token
            else:
                logger.error(f"❌ 토큰 발급 실패 - 상태코드: {res.status_code}")
                return None
        
        except Exception as e:
            logger.error(f"❌ 토큰 발급 오류: {e}")
            return None
    
    def ensure_token(self) -> str:
        """토큰이 없으면 발급"""
        if not self.access_token:
            token = self.get_access_token()
            if not token:
                raise Exception("토큰 발급 실패")
        return self.access_token
    
    def get_current_price(self, stock_code: str) -> Dict[str, Any]:
        """현재가 조회"""
        self.ensure_token()
        
        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {self.access_token}",
            "appkey": self.config['REAL_APP_KEY'],
            "appsecret": self.config['REAL_APP_SECRET'],
            "tr_id": "FHKST01010100"
        }
        
        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": stock_code
        }
        
        PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
        URL = f"{self.config['REAL_URL']}/{PATH}"
        
        res = requests.get(URL, headers=headers, params=params, timeout=10)
        
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception(f"API 호출 실패: {res.status_code}")
    # 추가    
    def get_stock_info(self, stock_code: str) -> Dict[str, Any]:
        """
        종목 기본 정보 조회 (시가총액 포함)
        """
        self.ensure_token()
        
        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {self.access_token}",
            "appkey": self.config['REAL_APP_KEY'],
            "appsecret": self.config['REAL_APP_SECRET'],
            "tr_id": "FHKST01010100"  # 주식현재가 시세
        }
        
        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": stock_code
        }
        
        PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
        URL = f"{self.config['REAL_URL']}/{PATH}"
        
        res = requests.get(URL, headers=headers, params=params, timeout=10)
        
        if res.status_code == 200:
            data = res.json()
            if data['rt_cd'] == '0':
                output = data['output']
                # 시가총액 계산: 현재가 * 상장주식수
                current_price = int(output['stck_prpr'])
                listed_shares = int(output.get('lstn_stcn', 0))  # 상장주식수
                market_cap = current_price * listed_shares if listed_shares > 0 else 0
                
                return {
                    'stock_code': stock_code,
                    'current_price': current_price,
                    'change': int(output['prdy_vrss']),
                    'change_rate': float(output['prdy_ctrt']),
                    'volume': int(output['acml_vol']),
                    'market_cap': market_cap,  # 시가총액 (원)
                    'listed_shares': listed_shares,  # 상장주식수
                    'per': output.get('per', '0'),
                    'pbr': output.get('pbr', '0')
                }
        
        raise Exception(f"API 호출 실패: {res.status_code}")

    def get_stock_chart(self, stock_code: str, period: str = "D") -> Dict[str, Any]:
        """차트 데이터 조회"""
        self.ensure_token()
        
        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {self.access_token}",
            "appkey": self.config['REAL_APP_KEY'],
            "appsecret": self.config['REAL_APP_SECRET'],
            "tr_id": "FHKST03010100"
        }
        
        end_date = datetime.now().strftime("%Y%m%d")
        period_days = {"D": 30, "W": 90, "M": 365, "Y": 365 * 3}
        days = period_days.get(period, 30)
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
        
        params = {
            "fid_cond_mrkt_div_code": "J",
            "fid_input_iscd": stock_code,
            "fid_input_date_1": start_date,
            "fid_input_date_2": end_date,
            "fid_period_div_code": period,
            "fid_org_adj_prc": "0"
        }
        
        PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        URL = f"{self.config['REAL_URL']}/{PATH}"
        
        res = requests.get(URL, headers=headers, params=params, timeout=10)
        
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception(f"차트 조회 실패: {res.status_code}")


# 싱글톤 인스턴스
ki_service = KoreaInvestmentService()
