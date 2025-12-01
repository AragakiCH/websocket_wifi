import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    # ctrlX
    CTRLX_HOST: str = "192.168.100.31"
    CTRLX_PORT: int = 8443
    CTRLX_USER: str = "boschrexroth"
    CTRLX_PASS: str = "boschrexroth"

    LOGBOOK_LIMIT: int = 500
    POLL_PERIOD_SEC: float = 2.0
    ONLY_PLC_MESSAGES: bool = False

    # OPC UA
    OPCUA_ENDPOINT: str = "opc.tcp://127.0.0.1:4840"
    OPCUA_ENABLED: bool = False

    # Servicio
    LOG_GATEWAY_PORT: int = 9000
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def base_url(self) -> str:
        return f"https://{self.CTRLX_HOST}:{self.CTRLX_PORT}"

    @property
    def logbook_url(self) -> str:
        return f"{self.base_url}/logbook/api/v2/entries"

    @property
    def token_url(self) -> str:
        return f"{self.base_url}/identity-manager/api/v1/auth/token"


@lru_cache
def get_settings() -> Settings:
    return Settings()
