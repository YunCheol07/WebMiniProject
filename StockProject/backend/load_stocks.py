import pandas as pd
from database import SessionLocal, Stock, init_db
import os

def load_stocks_from_excel(file_path: str):
    """
    Excel 파일에서 주식 종목 데이터를 읽어서 DB에 저장
    
    Excel 파일 형식:
    - A열: 단축코드 (stock_code)
    - B열: 한글명 (stock_name)
    """
    
    # 테이블이 없으면 생성
    init_db()
    
    # Excel 파일 읽기
    if not os.path.exists(file_path):
        print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
        return
    
    try:
        # Excel 파일 읽기
        df = pd.read_excel(file_path)
        
        print(f"📊 Excel 파일 로드 완료: {len(df)}개 행")
        print(f"컬럼: {list(df.columns)}")
        
        # 컬럼 확인
        if '단축코드' in df.columns and '한글명' in df.columns:
            code_col = '단축코드'
            name_col = '한글명'
        elif len(df.columns) >= 2:
            code_col = df.columns[0]
            name_col = df.columns[1]
        else:
            print(f"❌ 올바른 형식이 아닙니다. 최소 2개의 컬럼이 필요합니다.")
            return
        
        print(f"✅ 코드 컬럼: {code_col}, 이름 컬럼: {name_col}")
        
    except Exception as e:
        print(f"❌ Excel 파일 읽기 실패: {e}")
        return
    
    # DB 세션
    db = SessionLocal()
    
    added_count = 0
    updated_count = 0
    error_count = 0
    skipped_count = 0
    
    try:
        for idx, row in df.iterrows():
            try:
                stock_code_raw = str(row[code_col]).strip()
                stock_name = str(row[name_col]).strip()
                
                # 빈 값 체크
                if not stock_code_raw or stock_code_raw == 'nan':
                    skipped_count += 1
                    continue
                
                if not stock_name or stock_name == 'nan':
                    skipped_count += 1
                    continue
                
                # 종목코드 처리 (숫자만 있으면 6자리로 패딩, 아니면 그대로)
                if stock_code_raw.isdigit():
                    stock_code = stock_code_raw.zfill(6)
                else:
                    stock_code = stock_code_raw
                
                # 기존 데이터 확인
                existing_stock = db.query(Stock).filter(Stock.stock_code == stock_code).first()
                
                if existing_stock:
                    # 업데이트
                    existing_stock.stock_name = stock_name
                    updated_count += 1
                else:
                    # 신규 추가
                    new_stock = Stock(
                        stock_code=stock_code,
                        stock_name=stock_name
                    )
                    db.add(new_stock)
                    added_count += 1
                
                # 100개마다 커밋
                if (idx + 1) % 100 == 0:
                    db.commit()
                    print(f"진행: {idx + 1}/{len(df)} 종목 처리 중...")
                
            except Exception as e:
                print(f"❌ 행 {idx + 2} 처리 실패: {e}")
                error_count += 1
                continue
        
        # 최종 커밋
        db.commit()
        
        print("\n" + "="*60)
        print(f"✅ 종목 데이터 로드 완료!")
        print(f"📊 신규 추가: {added_count}개")
        print(f"🔄 업데이트: {updated_count}개")
        print(f"⏭️  건너뜀: {skipped_count}개")
        print(f"❌ 실패: {error_count}개")
        print(f"📈 총 DB 종목 수: {db.query(Stock).count()}개")
        print("="*60)
        
        # 샘플 데이터 출력
        print("\n샘플 데이터 (처음 5개):")
        sample_stocks = db.query(Stock).limit(5).all()
        for stock in sample_stocks:
            print(f"  - {stock.stock_code}: {stock.stock_name}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 데이터베이스 오류: {e}")
    
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("\n" + "="*60)
        print("📊 주식 종목 데이터 로드 스크립트")
        print("="*60)
        print("\n사용법:")
        print("  python load_stocks.py <excel_file_path>")
        print("\n예시:")
        print("  python load_stocks.py stocks.xlsx")
        print("\n파일 형식:")
        print("  - A열: 단축코드 (예: F70100009)")
        print("  - B열: 한글명 (예: 한투삼성그룹성장테마1호(A))")
        print("="*60 + "\n")
    else:
        file_path = sys.argv[1]
        load_stocks_from_excel(file_path)
