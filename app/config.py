from pydantic import BaseSettings


class _Settings(BaseSettings):
    SERVICE_NAME = "misollar_service"
    SERVICE_HOST = "localhost"
    SERVICE_PORT = ":9031"
    LOGS_PATH = "logs"
    API_KEY = "07be659f-5168-4c7e-ae3e-5130e06ea99a"


settings = _Settings()
