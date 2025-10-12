from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import RedirectResponse
from google.oauth2 import id_token
from google.auth.transport import requests
import httpx
from auth.jwt_generation import *
from config import *

env_variables = get_settings()

router = APIRouter(
    prefix='/api/v1/auth',
    tags=['Auth']
)

@router.get('/oauth')
def oauth():
    google_auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={env_variables.client_id}&redirect_uri={env_variables.redirect_url}&response_type=code&scope=openid email profile"

    return { "redirectUrl": google_auth_url }

@router.get('/callback')
async def auth_callback(code: str, request: Request, response: Response):
    token = env_variables.token_uri
    data = {
        'code': code,
        'client_id': env_variables.client_id,
        'client_secret': env_variables.client_secret,
        'redirect_uri': request.url_for('auth_callback'),
        'grant_type': 'authorization_code',
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(token, data=data)
        resp.raise_for_status()
        token_response = resp.json()

    id_token_value = token_response.get('id_token')
    if not id_token_value:
        raise HTTPException(status_code=400, detail="Missing id_token in response.")
    
    try:
        id_info = id_token.verify_oauth2_token(id_token_value, requests.Request(), env_variables.client_id)
        print('ID_INFO', id_info)
        jwt_token = generate_jwt(GoogleUser(**id_info))
        # Implement get or create user

        redirect_response = RedirectResponse(url=env_variables.fe_url)
        redirect_response.set_cookie(key="jwt_token", value=jwt_token)
        return redirect_response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid id_token: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

