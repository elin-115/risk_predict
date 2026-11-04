# DB 연결 설정 파일
# - engine        : DB와 실제로 연결을 맺는 객체
# - SessionFactory: 요청마다 세션(DB 작업 단위)을 만들어주는 공장
# - get_session   : 라우터에서 Depends 로 주입받아 쓰는 세션

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# DB 종류 + 사용할 드라이버 + 파일 경로
# sqlite(DB 종류) + aiosqlite(비동기 드라이버) + project.db(파일)
DATABASE_URL = "sqlite+aiosqlite:///project.db"

# echo=True : 실행되는 SQL 문을 터미널에 출력 (개발할 때 확인용)
engine = create_async_engine(DATABASE_URL, echo=True)

SessionFactory = async_sessionmaker(
    bind=engine,
    autoflush=False,          # 쿼리 전에 자동으로 flush 하지 않음
    autocommit=False,         # commit 은 직접 호출해야 반영됨
    expire_on_commit=False    # commit 후에도 객체 값을 그대로 쓸 수 있게 유지
)

# 요청 1개당 세션 1개를 열고, 요청이 끝나면 닫아줌
async def get_session():
    session = SessionFactory()

    try:
        yield session             # 함수를 끝내지 않고 세션을 라우터에 넘겨줌
    finally:
        await session.close()     # 요청 처리가 끝나면(에러가 나도) 세션 반납
