from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    SERVICE_NAME: str = "misollar_service"
    SERVICE_HOST: str = "localhost"
    SERVICE_PORT: str = ":9020"
    LOGS_PATH: str = "logs"
    API_KEY: str = "07be659f-5168-4c7e-ae3e-5130e06ea99a"


settings = _Settings()
