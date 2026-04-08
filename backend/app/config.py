from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Claude
    anthropic_api_key: str

    # Zoho Mail
    zoho_smtp_host: str = "smtppro.zoho.in"
    zoho_smtp_port: int = 465
    zoho_smtp_email: str
    zoho_smtp_password: str

    # Zoho Bigin (optional for now)
    bigin_access_token: str = ""
    bigin_refresh_token: str = ""
    bigin_client_id: str = ""
    bigin_client_secret: str = ""

    # Paths
    upload_dir: str = "./uploads"
    output_dir: str = "./outputs"

    class Config:
        env_file = ".env"


settings = Settings()