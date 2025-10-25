"""
JWT token generation and validation module for Finance Tracker API.

This module provides JWT token generation and validation functionality for the
Finance Tracker application. It handles creating secure JWT tokens for
authenticated users and validating existing tokens for authentication.

The module includes:
- JWT token generation with user information and expiration
- JWT token validation and decoding
- Secure token handling with configurable algorithms and secrets
"""

from datetime import datetime, timedelta, timezone
import jwt
from config import get_settings

from db.models.users_model import User

env_variables = get_settings()


def generate_jwt(user: User):
    """
    Generate a JWT token for the authenticated user.

    This function creates a secure JWT token containing user information
    and an expiration time. The token is signed using the application's
    secret key and configured algorithm.

    Args:
        user (User): The authenticated user object from the database

    Returns:
        str: Encoded JWT token string
    """
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

    encoded_jwt = jwt.encode(
        to_encode, env_variables.jwt_secret, env_variables.jwt_algo
    )
    return encoded_jwt


def decode_jwt(token: str):
    """
    Decode and validate a JWT token.

    This function decodes and validates a JWT token, extracting the
    user information contained within. It verifies the token's signature
    and expiration time.

    Args:
        token (str): The JWT token string to decode

    Returns:
        dict: Decoded token payload containing user information

    Raises:
        jwt.InvalidTokenError: If the token is invalid, expired, or malformed
    """
    return jwt.decode(token, env_variables.jwt_secret, env_variables.jwt_algo)
