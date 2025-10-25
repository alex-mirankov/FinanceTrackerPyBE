"""
Cookie middleware module for Finance Tracker API.

This module provides JWT-based authentication middleware that validates
JWT tokens from HTTP cookies and injects user information into the
request context. It handles authentication for all protected routes
while allowing public access to authentication endpoints.
"""

from jwt.exceptions import InvalidTokenError
from fastapi import status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from auth.jwt_generation import decode_jwt


class CookieMiddleware(BaseHTTPMiddleware):
    """
    JWT authentication middleware for cookie-based authentication.

    This middleware intercepts all incoming requests and validates JWT tokens
    stored in HTTP cookies. It provides automatic authentication for protected
    routes while allowing public access to authentication endpoints.

    The middleware:
    - Extracts JWT tokens from the 'jwt_token' cookie
    - Validates token authenticity and expiration
    - Injects user information into request context
    - Handles authentication errors with appropriate HTTP responses
    """

    async def dispatch(self, request, call_next):
        """
        Process incoming requests and handle JWT authentication.

        This method is called for every incoming request and performs the following:
        1. Check if the route requires authentication
        2. Extract and validate JWT token from cookies
        3. Decode token and extract user information
        4. Inject user info into request context
        5. Continue to the next middleware/handler

        Args:
            request: The incoming HTTP request object
            call_next: The next middleware/handler in the chain

        Returns:
            JSONResponse: Authentication error response if token is invalid/missing
            Response: The response from the next handler if authentication succeeds

        Authentication Flow:
        - Public routes (starting with "/api/v1/auth") and OPTIONS requests bypass authentication
        - Protected routes require a valid JWT token in the 'jwt_token' cookie
        - Invalid or missing tokens return 401 Unauthorized with error message
        - Valid tokens have user information injected into request.state.user_info
        """

        if request.url.path.startswith("/api/v1/auth") or request.method == "OPTIONS":
            return await call_next(request)

        jwt_token = request.cookies.get("jwt_token")
        if not jwt_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "No authentication credentials provided"},
            )

        try:
            user_info = decode_jwt(jwt_token)
        except InvalidTokenError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "No authentication credentials provided"},
            )

        request.state.user_info = user_info
        response = await call_next(request)
        return response
