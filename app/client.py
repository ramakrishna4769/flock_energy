import httpx

from app.config import settings


class UrjaPortalClient:

    def __init__(self):

        self.base_url = settings.BASE_URL.rstrip("/")
        self.username = settings.USERNAME
        self.password = settings.PASSWORD

        self.client = httpx.Client(
            timeout=settings.REQUEST_TIMEOUT,
            follow_redirects=True,
            headers={
                "User-Agent": settings.USER_AGENT,
                "Accept": "application/json"
            }
        )

        self.logged_in = False

    # -------------------------------
    # Login
    # -------------------------------

    def login(self):

        login_url = f"{self.base_url}{settings.LOGIN_ENDPOINT}"

        payload = {
            "email": self.username,
            "password": self.password
        }

        response = self.client.post(
            login_url,
            data=payload
        )

        if "Invalid email or password" in response.text:
            raise Exception("Invalid Credentials")

        self.logged_in = True

    # -------------------------------
    # Authentication
    # -------------------------------

    def ensure_authenticated(self):

        if not self.logged_in:
            self.login()

    # -------------------------------
    # Generic Request
    # -------------------------------

    def request(self, method, endpoint, **kwargs):

        self.ensure_authenticated()

        response = self.client.request(
            method,
            f"{self.base_url}{endpoint}",
            **kwargs
        )

        response.raise_for_status()

        return response

    # -------------------------------
    # Get Meters
    # -------------------------------

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