# 인증/인가 관련 함수 모음
# 인증 (Authentication) : 누구인지 식별   (로그인, 토큰 검증)
# 인가 (Authorization)  : 권한 부여       (이 사용자가 이 기능을 써도 되는지)

from datetime import datetime, timezone, timedelta

# 설치 필요  pip install bcrypt pyjwt
import bcrypt
import jwt

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

from config import settings

# str.encode():     str   -> bytes
# bytes.decode():   bytes -> str

# ---------------------------------------------------------------
# 비밀번호 해싱
# ---------------------------------------------------------------

# 평문 비밀번호 -> 해시 문자열 (DB에는 이 값만 저장)
def hash_password(plain_password: str) -> str:
    hashed_password: bytes = bcrypt.hashpw(
        plain_password.encode(),    # bcrypt 는 bytes 만 받음
        bcrypt.gensalt()            # salt(랜덤 값)를 섞어서 같은 비번도 매번 다른 해시가 나옴
    )
    return hashed_password.decode() # DB 저장용으로 다시 str 로 변환

# 로그인 시 입력한 비밀번호가 저장된 해시와 맞는지 확인
def verify_password(
    plain_password: str, password_hash: str
) -> bool:
    # 해시 안에 salt 가 들어 있어서, 같은 salt 로 다시 해싱해 비교해줌
    return bcrypt.checkpw(
        plain_password.encode(), password_hash.encode()
    )

# ---------------------------------------------------------------
# JWT (= JSON Web Token)
# 로그인 성공 시 발급하는 "출입증". 이후 요청 헤더에 넣어서 본인임을 증명
# ---------------------------------------------------------------

# 토큰 발급
def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),        # subject : 토큰의 주인(사용자 id). 문자열이어야 함
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),  # 24시간 뒤 만료
    }
    return jwt.encode(
        payload=payload,
        key=settings.jwt_secret_key,    # 이 비밀키로 서명 -> 위조 방지
        algorithm="HS256",
    )

# 토큰 검증 (서명이 맞는지, 만료되지 않았는지)
def verify_access_token(access_token:str):
    try:
        # TODO: 디코딩한 결과(payload)를 변수에 담아 return 해야
        #       verify_user 에서 payload.get("sub") 를 쓸 수 있음 (지금은 None 반환)
        jwt.decode(
        jwt=access_token,
        key=settings.jwt_secret_key, # 서명 확인
        algorithms=["HS256"]
        )
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="잘못된 토큰 형식입니다.")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="만료된 토큰입니다.")
    return

# HTTP 헤더에 인증 토큰이 있는지 검증 -> 로그인한 사용자 id 반환
# auth_header = {"Authorization": "Bearer xxxx"}
# 라우터에서 `user_id = Depends(verify_user)` 로 쓰면 토큰이 필요한 API 가 됨
def verify_user(
    auth_header = Depends(HTTPBearer())     # 헤더에서 "Bearer " 뒤의 토큰을 꺼내줌
):
    access_token = auth_header.credentials
    payload = verify_access_token(access_token=access_token)
    user_id = payload.get("sub")            # 토큰에 넣어둔 사용자 id
    if not user_id:
        raise HTTPException(
            status_code=401, detail="sub 값이 없습니다."
        )
    return int(user_id)
