from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_api_key: str
    upload_dir: str = "./uploads"
    output_dir: str = "./outputs"
    hashnode_api_key: str = ""
    hashnode_publication_id: str = ""
    
    class Config:
        env_file = ".env"


settings = Settings()