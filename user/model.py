# DB 테이블 모델 (SQLAlchemy ORM)
# 클래스 1개 = 테이블 1개, 속성 1개 = 컬럼 1개

from datetime import datetime

from database.orm import Base

from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Float, Boolean
from sqlalchemy.orm import mapped_column, Mapped

# 회원 테이블
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(                                # id            : 회원 번호 (자동 증가)
        Integer, primary_key=True, autoincrement=True
    )
    email: Mapped[str] = mapped_column(String(256), unique=True)    # unique=True   : 중복 X
    password_hash: Mapped[str] = mapped_column(String(256))         # password_hash : 비밀번호를 난독화해서 저장
    created_at: Mapped[datetime] = mapped_column(                   # created_at    : 행 생성 시간 저장
        DateTime, server_default=func.now()                         # server_default: DB가 저장할 때 시간을 채움
    )

# 건강 프로필 입력할 테이블 (예측 모델의 입력값)
class UserHealthProfile(Base):
    __tablename__ = "user_health_profile"

    id: Mapped[int] = mapped_column(
            Integer, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(           # 어떤 회원의 프로필인지 (user.id 참조)
        ForeignKey("user.id"), unique=True          # unique=True : 회원 1명당 프로필 1개
    )

    age: Mapped[int] = mapped_column(Integer)                   # 나이
    height_cm: Mapped[float] = mapped_column(Float)             # 키 (cm)
    weight_kg: Mapped[float] = mapped_column(Float)             # 몸무게 (kg)
    smoking: Mapped[bool] = mapped_column(Boolean)              # 흡연 여부
    exercise_per_week: Mapped[int] = mapped_column(Integer)     # 주당 운동 횟수

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
