from fastapi import HTTPException, status
from pydantic import BaseModel
import jwt
from config import *
from datetime import datetime, timedelta, timezone

from db.models.users_model import User

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

def generate_jwt(user: User):
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    to_encode = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "sub_id": user.sub_id,
        "picture": user.picture,
        "verified_email": user.verified_email,
        "exp": expire,
    }

    encoded_jwt = jwt.encode(to_encode, env_variables.jwt_secret, env_variables.jwt_algo)
    return encoded_jwt

def decode_jwt(token: str):
    return jwt.decode(token, env_variables.jwt_secret, env_variables.jwt_algo)