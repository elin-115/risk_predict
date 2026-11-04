# 요청 본문(Request Body) 양식 (Pydantic)
# 클라이언트가 보낸 JSON 을 이 양식대로 검사하고, 틀리면 FastAPI 가 422 에러를 돌려줌

from pydantic import BaseModel, EmailStr

# 회원가입 요청에 필요한 요청 본문 양식
class SignUpRequest(BaseModel):
    # 클라이언트에게 받아야하는 데이터 : email, password
    email: EmailStr     # 이메일 형식인지 자동 검사 (email-validator 패키지 필요)
    password: str

# 로그인 요청에 필요한 요청 본문 형식
class LogInRequest(BaseModel):
    email: EmailStr
    password: str

# 건강 프로필 생성에 필요한 요청 본문 형식
class CreateHealthProfileRequest(BaseModel):
    age: int                # 나이
    height_cm: float        # 키 (cm)
    weight_kg: float        # 몸무게 (kg)
    smoking: bool           # 흡연 여부
    exercise_per_week: int  # 주당 운동 횟수
