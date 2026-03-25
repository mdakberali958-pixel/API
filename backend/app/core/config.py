from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Hallucination-Aware AI"
    api_v1_prefix: str = "/api/v1"
    jwt_secret: str = "CHANGE_ME"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    rate_limit_per_minute: int = 60
    chroma_persist_dir: str = "./data/chroma"
    llm_model_standard: str = "gpt-4o-mini"
    llm_model_verified: str = "gpt-4.1-mini"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
