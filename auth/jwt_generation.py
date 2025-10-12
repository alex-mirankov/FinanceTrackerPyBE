from fastapi import HTTPException, status
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError
from config import *
from datetime import datetime, timedelta, timezone

env_variables = get_settings()

class GoogleUser(BaseModel):
    sub: str
    email: str
    email_verified: bool
    name: str
    picture: str
    given_name: str
    family_name: str
    exp: int


def generate_jwt(google_user: GoogleUser):
    to_encode = google_user.model_dump().copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode.update({ "exp": expire })
    encoded_jwt = jwt.encode(to_encode, env_variables.jwt_secret, env_variables.jwt_algo)
    return encoded_jwt

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, env_variables.jwt_secret, env_variables.jwt_algo)
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )