from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "local"
    log_level: str = "INFO"
    gemini_api_key: str
    gemini_model: str = "gemini-3.5-flash-lite"
    database_url: str


settings = Settings()