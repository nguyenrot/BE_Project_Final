import requests

from core.settings import (
    DEFAULT_CLIENT_SECRET,
    DEFAULT_CLIENT_ID,
    API_HOST,
    OAUTH_URL,
)


class AuthorizationOauth2:
    @classmethod
    def authorization_oauth2(cls, username, password=None, token=None):
        url = OAUTH_URL + "/api/o/token/"
        payload = {
            "client_type": "confidential",
            "grant_type": "password",
            "client_id": DEFAULT_CLIENT_ID,
            "client_secret": DEFAULT_CLIENT_SECRET,
            "username": username,
            "password": password,
            "token": token,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": API_HOST,
        }

        request_oauth2 = requests.post(url, data=payload, headers=headers)
        return request_oauth2

    @classmethod
    def refresh_token_view(cls, refresh_token):
        url = OAUTH_URL + "/api/o/token/"
        payload = {
            "grant_type": "refresh_token",
            "client_id": DEFAULT_CLIENT_ID,
            "client_secret": DEFAULT_CLIENT_SECRET,
            "refresh_token": refresh_token,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": API_HOST,
        }
        request_oauth2 = requests.post(url, data=payload, headers=headers)
        return request_oauth2

    @classmethod
    def logout_oauth2(cls, refresh_token, access_token):
        url = OAUTH_URL + "/api/o/revoke_token/"
        # revoke refresh_token first, to make user can not renew access_token
        payload = {
            "client_id": DEFAULT_CLIENT_ID,
            "client_secret": DEFAULT_CLIENT_SECRET,
            "token_type_hint": "refresh_token",
            "token": refresh_token,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": API_HOST,
        }
        r = requests.post(url, data=payload, headers=headers)
        if r.status_code != 200:
            return False
        # revoke access_token
        payload = {
            "client_id": DEFAULT_CLIENT_ID,
            "client_secret": DEFAULT_CLIENT_SECRET,
            "token_type_hint": "access_token",
            "token": access_token,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": API_HOST,
        }
        r = requests.post(url, data=payload, headers=headers)
        if r.status_code != 200:
            return False
        return True
