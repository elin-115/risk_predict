# 환경 변수(.env) 설정 파일
# - 비밀 값(API 키, JWT 비밀키)은 코드에 직접 쓰지 않고 .env 에서 읽어옴
# - .env 는 .gitignore 에 등록돼 있어 깃에 올라가지 않음

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 필드 이름은 .env 의 키 이름과 대소문자 무시하고 매칭됨
    # (openai_api_key <-> OPENAI_API_KEY)
    openai_api_key: str     # 문맥 관리(LLM)에 쓸 OpenAI API 키
    jwt_secret_key: str     # JWT 토큰 서명에 쓸 비밀키

    # 어떤 파일에서 값을 읽을지 지정
    model_config = SettingsConfigDict(env_file=".env")

# 다른 파일에서는 `from config import settings` 로 가져다 씀
settings = Settings()
