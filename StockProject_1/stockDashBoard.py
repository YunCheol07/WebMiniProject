# streamlit 테스트 버전
import streamlit as st
import requests
import json
import yaml
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 설정 파일 로드
@st.cache_resource
def load_config():
    with open('./stockinfo.yaml', encoding='UTF-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

# 접근 토큰 발급
@st.cache_data(ttl=3600)  # 1시간 캐시
def get_access_token(config):
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": config['REAL_APP_KEY'],
        "appsecret": config['REAL_APP_SECRET']
    }
    
    PATH = "oauth2/tokenP"
    URL = f"{config['REAL_URL']}/{PATH}"
    
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    
    if res.status_code == 200:
        return res.json()["access_token"]
    else:
        st.error(f"토큰 발급 실패: {res.status_code}")
        return None

# 주식 현재가 조회
def get_current_price(token, config, stock_code):
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
        "appkey": config['REAL_APP_KEY'],
        "appsecret": config['REAL_APP_SECRET'],
        "tr_id": "FHKST01010100"
    }
    
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": stock_code
    }
    
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{config['REAL_URL']}/{PATH}"
    
    res = requests.get(URL, headers=headers, params=params)
    
    if res.status_code == 200:
        return res.json()
    else:
        st.error(f"API 호출 실패: {res.status_code}")
        return None

# 일자별 시세 조회 함수
def get_stock_price_daily(token, config, stock_code, period="D"):
    """
    일자별 주가 데이터 조회
    period: D(일), W(주), M(월)
    """
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {token}",
        "appkey": config['REAL_APP_KEY'],
        "appsecret": config['REAL_APP_SECRET'],
        "tr_id": "FHKST03010100"
    }
    
    # 기간 설정
    end_date = datetime.now().strftime("%Y%m%d")
    
    if period == "D":
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
    elif period == "W":
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y%m%d")
    elif period == "M":
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
    elif period == "Y":
        start_date = (datetime.now() - timedelta(days=365*3)).strftime("%Y%m%d")
    else:
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
    
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": stock_code,
        "fid_input_date_1": start_date,
        "fid_input_date_2": end_date,
        "fid_period_div_code": period,
        "fid_org_adj_prc": "0"
    }
    
    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{config['REAL_URL']}/{PATH}"
    
    res = requests.get(URL, headers=headers, params=params)
    
    if res.status_code == 200:
        return res.json()
    else:
        st.error(f"시세 조회 실패: {res.status_code}")
        return None

# 차트 그리기 함수
def draw_stock_chart(data, stock_name, stock_code, period_name):
    """
    캔들스틱 차트 생성
    """
    if not data or data.get("rt_cd") != "0":
        st.error("차트 데이터를 가져올 수 없습니다.")
        return None
    
    output = data.get("output2", [])
    
    if not output:
        st.warning("차트 데이터가 없습니다.")
        return None
    
    # 데이터 역순 정렬 (날짜 오름차순)
    output = output[::-1]
    
    # 데이터프레임 생성
    df = pd.DataFrame(output)
    
    # 날짜 형식 변환
    df['stck_bsop_date'] = pd.to_datetime(df['stck_bsop_date'])
    
    # 숫자 변환
    df['stck_oprc'] = pd.to_numeric(df['stck_oprc'])
    df['stck_hgpr'] = pd.to_numeric(df['stck_hgpr'])
    df['stck_lwpr'] = pd.to_numeric(df['stck_lwpr'])
    df['stck_clpr'] = pd.to_numeric(df['stck_clpr'])
    df['acml_vol'] = pd.to_numeric(df['acml_vol'])
    
    # 캔들스틱 차트 생성
    fig = go.Figure()
    
    # 캔들스틱 추가
    fig.add_trace(go.Candlestick(
        x=df['stck_bsop_date'],
        open=df['stck_oprc'],
        high=df['stck_hgpr'],
        low=df['stck_lwpr'],
        close=df['stck_clpr'],
        name='주가',
        increasing_line_color='red',
        decreasing_line_color='blue'
    ))
    
    # 거래량 차트
    fig.add_trace(go.Bar(
        x=df['stck_bsop_date'],
        y=df['acml_vol'],
        name='거래량',
        marker_color='rgba(158,202,225,0.5)',
        yaxis='y2'
    ))
    
    # 레이아웃 설정
    fig.update_layout(
        title=f"{stock_name} ({stock_code}) - {period_name} 차트",
        yaxis_title='주가 (원)',
        xaxis_title='날짜',
        template='plotly_dark',
        height=600,
        xaxis_rangeslider_visible=False,
        yaxis2=dict(
            title='거래량',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        hovermode='x unified'
    )
    
    return fig

# Streamlit UI
def main():
    st.title("📈 한국투자증권 주식 현재가 조회")
    st.markdown("---")
    
    # 종목명 매핑 딕셔너리
    STOCK_NAMES = {
        "005930": "삼성전자",
        "000660": "SK하이닉스",
        "035420": "NAVER",
        "035720": "카카오",
        "005380": "현대차"
    }
    
    # 설정 로드
    try:
        config = load_config()
    except FileNotFoundError:
        st.error("stockinfo.yaml 파일을 찾을 수 없습니다.")
        return
    
    # 토큰 발급
    token = get_access_token(config)
    if not token:
        return
    
    st.success("✅ API 인증 성공")
    
    # 종목 코드 입력
    col1, col2 = st.columns([3, 1])
    with col1:
        stock_code = st.text_input(
            "종목코드 입력 (6자리)", 
            value="005930",
            help="예: 삼성전자(005930), SK하이닉스(000660)"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("🔍 조회", use_container_width=True)
    
    # 주요 종목 바로가기
    st.markdown("**주요 종목:**")
    cols = st.columns(5)
    popular_stocks = {
        "삼성전자": "005930",
        "SK하이닉스": "000660",
        "NAVER": "035420",
        "카카오": "035720",
        "현대차": "005380"
    }
    
    for idx, (name, code) in enumerate(popular_stocks.items()):
        if cols[idx].button(name, use_container_width=True):
            stock_code = code
            search_btn = True
    
    # 현재가 조회
    if search_btn and stock_code:
        with st.spinner("데이터 조회 중..."):
            data = get_current_price(token, config, stock_code)
            
            if data and data.get("rt_cd") == "0":
                output = data.get("output", {})
                
                # 종목명 가져오기
                stock_name = STOCK_NAMES.get(stock_code, f"종목코드 {stock_code}")
                sector = output.get('bstp_kor_isnm', '')
                
                # 주요 정보 표시
                st.markdown("---")
                st.subheader(f"📊 {stock_name} ({stock_code})")
                if sector:
                    st.caption(f"업종: {sector}")
                
                # 현재가 정보
                col1, col2, col3, col4 = st.columns(4)
                
                current_price = int(output['stck_prpr'])
                change = int(output['prdy_vrss'])
                change_rate = float(output['prdy_ctrt'])
                
                col1.metric("현재가", f"{current_price:,}원")
                col2.metric("전일대비", f"{change:+,}원", f"{change_rate:+.2f}%")
                col3.metric("시가", f"{int(output['stck_oprc']):,}원")
                col4.metric("거래량", f"{int(output['acml_vol']):,}주")
                
                # 차트 섹션
                st.markdown("---")
                st.markdown("### 📈 주가 차트")
                
                tab1, tab2, tab3, tab4 = st.tabs(["1개월", "3개월", "1년", "3년"])
                
                with tab1:
                    with st.spinner("1개월 차트 로딩 중..."):
                        chart_data = get_stock_price_daily(token, config, stock_code, "D")
                        if chart_data:
                            fig = draw_stock_chart(chart_data, stock_name, stock_code, "1개월")
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                
                with tab2:
                    with st.spinner("3개월 차트 로딩 중..."):
                        chart_data = get_stock_price_daily(token, config, stock_code, "W")
                        if chart_data:
                            fig = draw_stock_chart(chart_data, stock_name, stock_code, "3개월")
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                
                with tab3:
                    with st.spinner("1년 차트 로딩 중..."):
                        chart_data = get_stock_price_daily(token, config, stock_code, "M")
                        if chart_data:
                            fig = draw_stock_chart(chart_data, stock_name, stock_code, "1년")
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                
                with tab4:
                    with st.spinner("3년 차트 로딩 중..."):
                        chart_data = get_stock_price_daily(token, config, stock_code, "Y")
                        if chart_data:
                            fig = draw_stock_chart(chart_data, stock_name, stock_code, "3년")
                            if fig:
                                st.plotly_chart(fig, use_container_width=True)
                
                # 상세 정보
                st.markdown("---")
                st.markdown("**상세 정보**")
                
                detail_col1, detail_col2, detail_col3 = st.columns(3)
                
                with detail_col1:
                    st.write(f"고가: **{int(output['stck_hgpr']):,}원**")
                    st.write(f"저가: **{int(output['stck_lwpr']):,}원**")
                
                with detail_col2:
                    st.write(f"52주 최고가: **{int(output['w52_hgpr']):,}원**")
                    st.write(f"52주 최저가: **{int(output['w52_lwpr']):,}원**")
                
                with detail_col3:
                    st.write(f"시가총액: **{int(output['hts_avls']):,}백만원**")
                    st.write(f"상장주식수: **{int(output['lstn_stcn']):,}주**")
                
                # 투자지표
                st.markdown("---")
                st.markdown("**투자지표**")
                
                indicator_col1, indicator_col2, indicator_col3, indicator_col4 = st.columns(4)
                
                with indicator_col1:
                    st.metric("PER", f"{float(output['per']):.2f}")
                
                with indicator_col2:
                    st.metric("PBR", f"{float(output['pbr']):.2f}")
                
                with indicator_col3:
                    st.metric("EPS", f"{float(output['eps']):,.0f}원")
                
                with indicator_col4:
                    st.metric("BPS", f"{float(output['bps']):,.0f}원")
                
            else:
                st.error("종목 정보를 가져오는데 실패했습니다. 종목코드를 확인해주세요.")

if __name__ == "__main__":
    main()
