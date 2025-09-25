import json
from abc import ABC, abstractmethod
from typing import Any

from flask import current_app
from jose import jwt
from six.moves.urllib.request import urlopen

from src.exception import AuthHttpException


class IAuth0Client(ABC):
    @property
    @abstractmethod
    def auth0_id(self):
        pass


class Auth0Client(IAuth0Client):
    def __init__(self, auth_header: str):
        token = get_token_auth_header(auth_header)

        # auth0 OfficialDocument
        # ref : https://github.com/auth0/auth0-python
        """
        NOTE
        # https://auth0.com/docs/tokens/guides/locate-jwks
        # https://community.auth0.com/t/caching-jwks-signing-key/17654
        https://auth0.com/docs/tokens/json-web-tokens/json-web-key-sets/locate-json-web-key-sets
        """

        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError as e:
            raise AuthHttpException(messages=["invalid JWT"]) from e

        self.unverified_header = unverified_header
        self.token = token

    @property
    def get_cached_jwks(self) -> Any:
        return json.loads(current_app.config["AUTH0_JWKS"])

    @property
    def get_jwks_from_well_known_path(self) -> Any:
        jsonurl = urlopen("https://{domain}/.well-known/jwks.json".format(domain=current_app.config["AUTH0_DOMAIN"]))
        return json.loads(jsonurl.read())

    @property
    def auth0_id(self) -> str:
        jwks = self.get_jwks(self.unverified_header["kid"])
        rsa_key = self.make_rsa_key(jwks, self.unverified_header)
        if not rsa_key:
            raise AuthHttpException(messages=["invalid_header, Unable to parse authentication token."])
        auth0_id = self._get_auth0_id(self.token, rsa_key)
        return auth0_id

    def get_jwks(self, jwt_kid: str):
        cached = self.get_cached_jwks
        if any(c["kid"] == jwt_kid for c in cached["keys"]):
            return cached
        else:
            current_app.logger.warning("JWK cache mishit")
            return self.get_jwks_from_well_known_path

    def make_rsa_key(self, jwks: dict, unverified_header: dict) -> dict:
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        return rsa_key

    def _get_auth0_id(self, token: str, rsa_key: dict) -> str:
        try:
            payload = jwt.decode(
                token=token,
                key=rsa_key,
                algorithms=["RS256"],
                audience=current_app.config["AUTH0_API_AUDIENCE"],
                issuer="https://{domain}/".format(domain=current_app.config["AUTH0_DOMAIN"]),
            )
            return str(payload["sub"])
        except jwt.ExpiredSignatureError as e:
            raise AuthHttpException(messages=["token is expired"]) from e
        except jwt.JWTClaimsError as e:
            raise AuthHttpException(messages=["incorrect claims please check the audience and issuer"]) from e
        except Exception as e:
            raise AuthHttpException(messages=["invalid_header"]) from e


def get_token_auth_header(auth_header: str) -> str:
    if not auth_header:
        raise AuthHttpException(messages=["Authorization header is expected"])

    parts = auth_header.split()

    if parts[0].lower() != "bearer":
        raise AuthHttpException(messages=["Authorization header must start with Bearer"])
    elif len(parts) == 1:
        raise AuthHttpException(messages=["Token not found"])
    elif len(parts) > 2:
        raise AuthHttpException(messages=["Authorization header must be Bearer token"])

    token = parts[1]
    return token


class StubAuth0Client(IAuth0Client):
    def __init__(self, auth_header: str):
        pass

    @property
    def auth0_id(self) -> str:
        return "auth|test"
