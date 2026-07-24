from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(frozen=True)
class Settings:

    BASE_URL = os.getenv(
        "URJA_BASE_URL",
        "https://urja-ops.flockenergy.tech"
    )

    LOGIN_ENDPOINT = os.getenv(
        "LOGIN_ENDPOINT",
        "/login"
    )

    METERS_ENDPOINT = os.getenv(
        "METERS_ENDPOINT",
        "/portal/meters/search"
    )

    USERNAME = os.getenv(
        "URJA_USERNAME",
        ""
    )

    PASSWORD = os.getenv(
        "URJA_PASSWORD",
        ""
    )

    REQUEST_TIMEOUT = int(
        os.getenv(
            "REQUEST_TIMEOUT",
            "30"
        )
    )

    USER_AGENT = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )


settings = Settings()