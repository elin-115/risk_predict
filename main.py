# FastAPI 앱 시작 파일
# 실행: fastapi dev main.py  ->  http://127.0.0.1:8000/docs 에서 API 테스트

from fastapi import FastAPI

from user.router import router as user_router
from prediction.router import router as prediction_router   # 예측 기능 구현 후 주석 해제

app = FastAPI(title="건강 예측 API")

# 기능별로 나눈 라우터를 앱에 등록
app.include_router(user_router)             # 회원가입 / 로그인 / 건강 프로필
app.include_router(prediction_router)       # 비만 / 고혈압 예측
