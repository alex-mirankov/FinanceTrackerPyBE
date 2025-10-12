from fastapi import FastAPI
from entities.transactions import router as transaction_router
from auth.auth import router as auth_router
from entities.users import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from middlewares.cookie_middleware import CookieMiddleware
from db.connect import *

origins = [
    'http://localhost:5173',
    'https://accounts.google.com',
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CookieMiddleware)

app.include_router(auth_router)
app.include_router(transaction_router)
app.include_router(user_router)

@app.get("/")
async def root():
    get_db()
    return {"message": "Hello World"}