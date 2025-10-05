from database import Base, engine, SessionLocal, Stock
import sys

def recreate_database():
    """
    기존 테이블을 모두 삭제하고 새로운 구조로 재생성
    
    주의: 모든 데이터가 삭제됩니다!
    """
    
    print("\n" + "="*60)
    print("⚠️  경고: 모든 데이터베이스 테이블이 삭제됩니다!")
    print("="*60)
    
    # 사용자 확인
    response = input("\n계속하시겠습니까? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("❌ 취소되었습니다.")
        return
    
    try:
        # 1. 모든 테이블 삭제
        print("\n🗑️  기존 테이블 삭제 중...")
        Base.metadata.drop_all(bind=engine)
        print("✅ 기존 테이블 삭제 완료")
        
        # 2. 새 테이블 생성
        print("\n📦 새 테이블 생성 중...")
        Base.metadata.create_all(bind=engine)
        print("✅ 새 테이블 생성 완료")
        
        # 3. 생성된 테이블 확인
        print("\n📊 생성된 테이블:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
        
        print("\n" + "="*60)
        print("✅ 데이터베이스 재생성 완료!")
        print("="*60)
        print("\n다음 단계:")
        print("  1. python load_stocks.py kospi_code_name.xlsx")
        print("  2. uvicorn app:app --reload")
        print()
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    recreate_database()