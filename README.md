# 건강 예측 API (risk_predict)

키, 몸무게, 나이, 흡연 여부 같은 건강 정보를 입력받아 **비만·고혈압 위험을 예측**하는 FastAPI 백엔드입니다.

## 기능
- 회원가입 / 로그인 (bcrypt 비밀번호 해싱, JWT 인증)
- 건강 프로필 등록 (진행 중)
- 비만·고혈압 예측 (예정)
- 문맥 관리 — LLM 연결 (예정)

## 기술 스택
FastAPI · SQLAlchemy 2 (async) · SQLite(aiosqlite) · Pydantic · bcrypt · PyJWT

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

## 문서 (docs)
| 문서 | 내용 | 보기 |
|---|---|---|
| [진행상황.md](docs/%EC%A7%84%ED%96%89%EC%83%81%ED%99%A9.md) | 전체 진행 현황, 단계별 구현 기록, 남은 작업 | GitHub에서 바로 보기 |
| [day1_2_인증과_건강프로필.html](docs/day1_2_%EC%9D%B8%EC%A6%9D%EA%B3%BC_%EA%B1%B4%EA%B0%95%ED%94%84%EB%A1%9C%ED%95%84.html) | 1~2일차 정리: 회원가입·로그인·JWT 인증, 건강 프로필 테이블, 에러 기록 | [웹페이지로 보기](https://htmlpreview.github.io/?https://github.com/elin-115/risk_predict/blob/main/docs/day1_2_%EC%9D%B8%EC%A6%9D%EA%B3%BC_%EA%B1%B4%EA%B0%95%ED%94%84%EB%A1%9C%ED%95%84.html) |

> HTML 문서는 GitHub에서 코드로 보이므로 "웹페이지로 보기" 링크로 열거나, 내려받아 브라우저로 열면 된다.
