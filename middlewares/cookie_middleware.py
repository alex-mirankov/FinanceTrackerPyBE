from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from auth.jwt_generation import *

class CookieMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path.startswith("/api/v1/auth") or request.method == "OPTIONS":
            return await call_next(request)

        jwt_token = request.cookies.get('jwt_token')
        if not jwt_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No authentication credentials provided",
            )
        user_info = decode_jwt(jwt_token)
        request.state.user_info = user_info
        response = await call_next(request)
        return response