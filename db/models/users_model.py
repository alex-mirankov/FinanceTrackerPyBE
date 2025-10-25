"""
Users model for Finance Tracker API.

This module defines the SQLAlchemy model for users in the
Finance Tracker application. Users represent authenticated individuals
who can create and manage their financial data including transactions,
categories, and finance periods.
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
from db.connect import Base


class User(Base):
    """
    SQLAlchemy model for users.
    
    This model represents authenticated users in the Finance Tracker
    application. Users are the central entity that owns and manages
    all financial data including transactions, categories, and periods.
    
    Attributes:
        id (int): Primary key identifier for the user
        name (str): Full name of the user
        email (str): Email address of the user
        sub_id (str): External authentication provider user ID (e.g., Auth0)
        picture (str): URL to the user's profile picture
        verified_email (bool): Whether the user's email is verified (defaults to False)
        
    Table: users
    
    Relationships:
        - Referenced by multiple models as the owner of financial data
        - One-to-many with Transaction, TransactionCategory, FinancePeriod, etc.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    sub_id: Mapped[str] = mapped_column(String, nullable=False)
    picture: Mapped[str] = mapped_column(String, nullable=False)
    verified_email: Mapped[bool] = mapped_column(Boolean, server_default="FALSE")
