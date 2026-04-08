from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_api_key: str
    upload_dir: str = "./uploads"
    output_dir: str = "./outputs"

    class Config:
        env_file = ".env"


settings = Settings()