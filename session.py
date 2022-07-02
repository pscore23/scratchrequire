import json
import re
import warnings

import requests
from requests import Response

import _common as c
import _exceptions as ex


class Session:
    def __init__(self, username: str = None, password: str = None) -> None:
        self.username = username
        self.password = password
        self.sessions_id = ""
        self.x_token = ""
        self.csrf_token = ""
        self.is_login = None
        self.headers = {}

        if (self.username is not None) and (self.password is not None):
            self._login()
            self.is_login = True
        else:
            warnings.warn("""
            ScratchRequire without login.
            Some functions are not available.
            """)
            self.is_login = False

    def _login(self) -> None:
        headers = {
            "x-csrftoken": "a",
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
            "referer": "https://scratch.mit.edu",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.101 Safari/537.36 "
        }
        data = json.dumps({"username": self.username, "password": self.password})
        req = requests.post(c.login_url, data=data, headers=headers)

        try:
            req.json()
        except Exception:
            if req.status_code == 403:
                raise ex.LoginFailed("""
                Login from this device has been denied.
                The following possibilities are available:
                Your IP address may be blocked - you often can't login from Replit
                """)
            else:
                raise ex.UnknownError("""
                An unknown error has occurred.
                Please wait a moment and try again...
                """)
