from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from auth.jwt_generation import *
from jwt.exceptions import InvalidTokenError

class CookieMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path.startswith("/api/v1/auth") or request.method == "OPTIONS":
            return await call_next(request)

        jwt_token = request.cookies.get('jwt_token')
        if not jwt_token:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message":"No authentication credentials provided"})
        try:
            user_info = decode_jwt(jwt_token)
        except InvalidTokenError:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message":"No authentication credentials provided"})

        request.state.user_info = user_info
        response = await call_next(request)
        return response