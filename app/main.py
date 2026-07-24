from fastapi import FastAPI, HTTPException
import httpx
from dataclasses import dataclass
from dotenv import load_dotenv
import os

# ===========================
# Load Environment Variables
# ===========================
load_dotenv()

@dataclass(frozen=True)
class Settings:
    BASE_URL = os.getenv("URJA_BASE_URL", "https://urja-ops.flockenergy.tech")
    LOGIN_ENDPOINT = os.getenv("LOGIN_ENDPOINT", "/login")
    METERS_ENDPOINT = os.getenv("METERS_ENDPOINT", "/portal/meters/search")
    USERNAME = os.getenv("URJA_USERNAME", "")
    PASSWORD = os.getenv("URJA_PASSWORD", "")
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    USER_AGENT = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    )

settings = Settings()

# ===========================
# FastAPI App
# ===========================
app = FastAPI(title="Urja Meter Ops Wrapper API")

# ===========================
# Urja Client
# ===========================
class UrjaPortalClient:

    def __init__(self):
        self.base_url = settings.BASE_URL.rstrip("/")
        self.username = settings.USERNAME
        self.password = settings.PASSWORD
        self.logged_in = False

        self.client = httpx.Client(
            timeout=settings.REQUEST_TIMEOUT,
            follow_redirects=True,
            headers={
                "User-Agent": settings.USER_AGENT,
                "Accept": "application/json"
            }
        )

    def login(self):
        login_url = f"{self.base_url}{settings.LOGIN_ENDPOINT}"

        payload = {
            "email": self.username,
            "password": self.password
        }

        print("=" * 50)
        print("LOGIN URL:", login_url)

        response = self.client.post(
            login_url,
            data=payload
        )

        print("STATUS:", response.status_code)
        print("COOKIES:", self.client.cookies)
        print("RESPONSE:", response.text[:500])
        print("=" * 50)

        if response.status_code >= 400:
            raise Exception("Login Failed")

        self.logged_in = True

    def ensure_authenticated(self):
        if not self.logged_in:
            self.login()

    def request(self, method, endpoint, **kwargs):
        self.ensure_authenticated()

        response = self.client.request(
            method,
            f"{self.base_url}{endpoint}",
            **kwargs
        )

        response.raise_for_status()

        return response

    def get_meters(self):
        response = self.request(
            "GET",
            settings.METERS_ENDPOINT,
            params={
                "q": "",
                "page": 1
            },
            headers={
                "Accept": "application/json"
            }
        )

        return response.json()


portal = UrjaPortalClient()

# ===========================
# API Routes
# ===========================

@app.get("/")
def home():
    return {
        "message": "Urja Meter Ops Wrapper API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/meters")
def get_meters():
    try:
        return portal.get_meters()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )