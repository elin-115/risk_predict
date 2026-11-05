# 응답 본문(Response Body) 양식 (Pydantic)
# 라우터의 response_model 로 지정하면, 여기 적힌 필드만 응답으로 나감
# -> password_hash 같은 민감한 값이 실수로 나가는 걸 막아줌

from datetime import datetime

from pydantic import BaseModel, ConfigDict

# 회원가입 응답에서 반환할 데이터 형식
class SignUpResponse(BaseModel):
    # from_attributes=True : dict 가 아니라 ORM 객체(User)의 속성을 읽어서 응답을 만듦
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    created_at: datetime

# 로그인 응답에서 반환할 데이터 형식
class LogInResponse(BaseModel):
    access_token: str       # 발급한 JWT 토큰

# 프로필 생성 응답에 반환할 데이터 현식
class UserHealthProfileResponse(BaseModel):
    id: int
    user_id: int
    height_cm: float
    weight_kg: float
    age: int
    smoking: bool
    exercise_per_week: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
