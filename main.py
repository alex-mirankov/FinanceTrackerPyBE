"""
Finance Tracker API - Main Application Module.

This module serves as the entry point for the Finance Tracker FastAPI application.

Architecture:
- FastAPI web framework
- SQLAlchemy ORM for database operations
- JWT authentication with cookie-based sessions
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.auth import router as auth_router
from entities.finance_periods import router as finance_periods_router
from entities.transaction_categories import router as transaction_categories_router
from entities.transactions import router as transactions_router
from middlewares.cookie_middleware import CookieMiddleware

origins = [
    "http://localhost:5173",
    "https://accounts.google.com",
]

app = FastAPI(
    title="Finance Tracker API",
    description="A comprehensive financial management API for tracking transactions, categories, and finance periods",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(CookieMiddleware)

app.include_router(auth_router)
app.include_router(transactions_router)
app.include_router(transaction_categories_router)
app.include_router(finance_periods_router)
