# ORM 기본 설정 파일
# - Base   : 모든 테이블 모델이 상속받는 부모 클래스
# - init_db: Base 를 상속한 모델들을 실제 DB 테이블로 생성

from database.connection import engine
from sqlalchemy.orm import DeclarativeBase


# 이 클래스를 상속한 모델은 Base.metadata 에 자동 등록됨
class Base(DeclarativeBase):
    pass

# 테이블 생성 함수
# - 모델 파일을 먼저 import 해야 Base.metadata 에 등록돼서 테이블이 만들어짐
# - 이미 있는 테이블은 건너뜀 (컬럼 변경은 반영 안 됨)
# 사용: python -m asyncio 에서 `await init_db()`  (괄호 필수)
async def init_db():
    async with engine.begin() as conn:
        # create_all 은 동기 함수라서 run_sync 로 감싸서 실행
        await conn.run_sync(Base.metadata.create_all)
