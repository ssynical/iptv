from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    secret_key: str
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "iptv_backend"
    
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    admin_username: str = "admin"
    admin_password: str

    class Config:
        env_file = ".env"

settings = Settings()