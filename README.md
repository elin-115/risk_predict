# 건강 예측 API (risk_predict)

나이, 키, 몸무게, 흡연 여부, 운동 횟수 같은 건강 정보를 OpenAI에 보내 **당뇨·고혈압 위험도를 예측**하는 FastAPI 백엔드입니다.

## 기능
- 회원가입 / 로그인 (bcrypt 비밀번호 해싱, JWT 인증)
- 건강 프로필 등록 (회원당 1개)
- 당뇨·고혈압 위험도 예측 (OpenAI 구조화된 출력, 24시간에 1번)

## 기술 스택
FastAPI · SQLAlchemy 2 (async) · SQLite(aiosqlite) · Pydantic · bcrypt · PyJWT · OpenAI

## 실행 방법
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # OPENAI_API_KEY, JWT_SECRET_KEY 값 채우기
```

테이블 생성
```bash
python -m asyncio
>>> from database.orm import init_db
>>> from user.model import User, UserHealthProfile
>>> from prediction.model import HealthRiskPrediction
>>> await init_db()
```

서버 실행
```bash
fastapi dev main.py         # http://127.0.0.1:8000/docs
```

## API
| Method | Path | 설명 | 인증 |
|---|---|---|---|
| POST | `/users` | 회원가입 | - |
| POST | `/users/login` | 로그인, JWT 발급 | - |
| POST | `/health-profiles` | 건강 프로필 생성 | Bearer 토큰 |
| POST | `/predictions` | 당뇨·고혈압 위험도 예측 (본문: `{"model_version": "gpt-5-mini"}`) | Bearer 토큰 |

## 문서 (docs)
| 문서 | 내용 | 보기 |
|---|---|---|
| [진행상황.md](docs/%EC%A7%84%ED%96%89%EC%83%81%ED%99%A9.md) | 전체 진행 현황, 단계별 구현 기록, 남은 작업 | GitHub에서 바로 보기 |
| [day1_2_인증과_건강프로필.html](docs/day1_2_%EC%9D%B8%EC%A6%9D%EA%B3%BC_%EA%B1%B4%EA%B0%95%ED%94%84%EB%A1%9C%ED%95%84.html) | 1~2일차 정리: 회원가입·로그인·JWT 인증, 건강 프로필 테이블, 에러 기록 | [웹페이지로 보기](https://htmlpreview.github.io/?https://github.com/elin-115/risk_predict/blob/main/docs/day1_2_%EC%9D%B8%EC%A6%9D%EA%B3%BC_%EA%B1%B4%EA%B0%95%ED%94%84%EB%A1%9C%ED%95%84.html) |
| [day3_건강프로필과_위험도예측.html](docs/day3_%EA%B1%B4%EA%B0%95%ED%94%84%EB%A1%9C%ED%95%84%EA%B3%BC_%EC%9C%84%ED%97%98%EB%8F%84%EC%98%88%EC%B8%A1.html) | 3일차 정리: 건강 프로필 저장, 예측 테이블, OpenAI 구조화된 출력, 24시간 제한, 에러 기록 | [웹페이지로 보기](https://htmlpreview.github.io/?https://github.com/elin-115/risk_predict/blob/main/docs/day3_%EA%B1%B4%EA%B0%95%ED%94%84%EB%A1%9C%ED%95%84%EA%B3%BC_%EC%9C%84%ED%97%98%EB%8F%84%EC%98%88%EC%B8%A1.html) |

> HTML 문서는 GitHub에서 코드로 보이므로 "웹페이지로 보기" 링크로 열거나, 내려받아 브라우저로 열면 된다.
