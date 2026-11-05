# 회원 관련 API (회원가입 / 로그인 / 건강 프로필)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from database.connection import get_session
from user.auth import hash_password, verify_password, create_access_token, verify_user
from user.model import User, UserHealthProfile
from user.request import SignUpRequest, LogInRequest, CreateHealthProfileRequest
from user.response import SignUpResponse, LogInResponse, UserHealthProfileResponse

router = APIRouter(tags=["User"])

# ---------------------------------------------------------------
# 회원가입 : 사용자 정보를 DB에 저장
# ---------------------------------------------------------------
@router.post(
    "/users",
    summary="회원가입 API",
    status_code=201,                 # 201 Created : 요청이 성공해서 새 데이터가 생성됨
    response_model=SignUpResponse    # 응답으로 id, email, created_at 만 내보냄 (비번 해시 제외)
)

async def sign_up_handler(
    body: SignUpRequest,                # 요청 본문 (email, password)
    session = Depends(get_session),     # 요청마다 DB 세션을 주입받음
):
    # [1] email 중복 검사
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    user = result.scalar()              # 결과가 없으면 None
    if user:
        raise HTTPException(
            status_code=409, detail="이미 가입된 이메일입니다."   # 409 Conflict : 이미 있는 데이터와 충돌
        )

    # [2] 비밀번호 해싱 (평문은 절대 저장하지 않음)
    password_hash = hash_password(plain_password=body.password)

    # [3] 회원 데이터 저장
    new_user = User(email=body.email, password_hash=password_hash)
    session.add(new_user)
    await session.commit()              # DB에 실제로 반영
    await session.refresh(new_user)     # DB가 채운 id, created_at 을 객체로 다시 읽어옴
    return new_user                     # response_model 이 필요한 필드만 골라서 응답

# ---------------------------------------------------------------
# 로그인 : 이메일/비밀번호 확인 후 JWT 토큰 발급
# ---------------------------------------------------------------
@router.post(
    "/users/login",
    summary="로그인 API",
    response_model=LogInResponse,
)

async def login_handler(
    body: LogInRequest,
    session = Depends(get_session),
):
    # [1] email로 사용자 조회(회원가입 여부 확인)
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    user = result.scalar()
    if not user:
        # 이메일이 없는지 비번이 틀렸는지 구분해서 알려주지 않음 (보안상 같은 메시지)
        raise HTTPException(
            status_code=401, detail="이메일과 비밀번호가 잘못 되었습니다"
        )

    # [2] 비밀번호 검증(body.password <> user.password_hash)
    is_verified = verify_password(
        plain_password=body.password, password_hash=user.password_hash,
    )
    if not is_verified:
        raise HTTPException(
            status_code=401, detail="이메일과 비밀번호가 잘못 되었습니다."   # 401 Unauthorized : 인증 실패
        )

    # [3] 임시 토큰(JWT) 발급
    access_token: str = create_access_token(user_id=user.id)
    return {
        "access_token": access_token
    }

# ---------------------------------------------------------------
# 건강 프로필 생성 : 로그인한 사용자만 가능 (JWT 필요)
# ---------------------------------------------------------------
@router.post(
    "/health-profiles",
    summary="건강 프로필 생성 API",
    status_code=201,
    response_model=UserHealthProfileResponse,      # 프로필 응답 양식 만들어서 지정
)
async def create_user_health_profile_handler(
    body: CreateHealthProfileRequest,   # 나이, 키, 몸무게, 흡연, 운동 횟수
    session = Depends(get_session),
    user_id = Depends(verify_user),     # 헤더에 JWT 토큰을 요구하도록 명시 -> 토큰의 사용자 id
):
    # [1] 프로필 중복 확인
    stmt = (
        select(UserHealthProfile)
        .where(UserHealthProfile.user_id == user_id)
    )
    result = await session.execute(stmt)
    profile = result.scalar()
    if profile:
        raise HTTPException(
            status_code=409, detail="이미 건강 프로필이 존재합니다."
        )

    # [2] UserHealthProfile 저장 -> 응답
    profile_data = body.model_dump()    # 딕셔너리로 바꿔줌
    new_profile = UserHealthProfile(user_id=user_id, **profile_data)
    session.add(new_profile)
    await session.commit()
    await session.refresh(new_profile)

    return new_profile
