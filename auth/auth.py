"""
Authentication module for Finance Tracker API.

This module provides OAuth2 authentication endpoints for the Finance Tracker
application using Google OAuth2. It handles the complete authentication flow
including user registration, JWT token generation, and secure cookie management.

The authentication flow:
1. User initiates OAuth with Google
2. Google redirects back with authorization code
3. Exchange code for access token and ID token
4. Verify ID token and extract user information
5. Create or retrieve user from database
6. Generate JWT token and set secure cookie
7. Redirect user to frontend application

Endpoints:
- GET /api/v1/auth/oauth: Initiate Google OAuth2 authentication
- GET /api/v1/auth/callback: Handle OAuth2 callback from Google
"""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from google.oauth2 import id_token
from google.auth.transport import requests as auth_requests
import httpx
from auth.jwt_generation import generate_jwt
from config import get_settings

from db.connect import get_db
from db.models.users_model import User

env_variables = get_settings()

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.get("/oauth")
def oauth():
    """
    Initiate Google OAuth2 authentication flow.

    This endpoint generates a Google OAuth2 authorization URL that the client
    can use to redirect users to Google's authentication service. The URL
    includes the necessary parameters for OAuth2 authorization code flow.

    Returns:
        dict: JSON response containing the Google OAuth2 redirect URL

    Example:
        GET /api/v1/auth/oauth
        Returns: {
            "redirectUrl": "URL"
        }

    OAuth2 Flow:
        1. Client calls this endpoint to get the authorization URL
        2. Client redirects user to the provided URL
        3. User authenticates with Google
        4. Google redirects to the callback endpoint with authorization code
    """
    google_auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={env_variables.client_id}&redirect_uri={env_variables.redirect_url}&response_type=code&scope=openid email profile"

    return {"redirectUrl": google_auth_url}


@router.get("/callback")
async def auth_callback(code: str, request: Request, db: Session = Depends(get_db)):
    """
    Handle OAuth2 callback from Google.

    This endpoint processes the authorization code returned by Google after
    user authentication. It exchanges the code for an access token, verifies
    the ID token, creates or retrieves the user, and generates a JWT token
    for the application.

    Args:
        code (str): Authorization code from Google OAuth2
        request (Request): FastAPI request object
        db (Session): Database session dependency

    Returns:
        RedirectResponse: Redirect to frontend with JWT cookie set

    Raises:
        HTTPException: 400 Bad Request if ID token is missing or invalid
        HTTPException: 500 Internal Server Error if authentication fails
    """
    token = env_variables.token_uri
    data = {
        "code": code,
        "client_id": env_variables.client_id,
        "client_secret": env_variables.client_secret,
        "redirect_uri": request.url_for("auth_callback"),
        "grant_type": "authorization_code",
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(token, data=data)
        resp.raise_for_status()
        token_response = resp.json()

    id_token_value = token_response.get("id_token")
    if not id_token_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing id_token in response.",
        )

    try:
        user_info = id_token.verify_oauth2_token(
            id_token_value, auth_requests.Request(), env_variables.client_id
        )
        user = db.query(User).filter_by(sub_id=user_info["sub"]).first()
        if not user:
            user = User(
                sub_id=user_info["sub"],
                email=user_info["email"],
                name=user_info["name"],
                picture=user_info["picture"],
                verified_email=user_info["email_verified"],
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        jwt_token = generate_jwt(user)
        redirect_response = RedirectResponse(url=env_variables.fe_url)
        redirect_response.set_cookie(
            key="jwt_token", value=jwt_token, secure=True, httponly=True
        )
        return redirect_response

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid id_token: {str(e)}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
