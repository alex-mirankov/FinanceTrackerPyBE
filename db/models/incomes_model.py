"""
Incomes model for Finance Tracker API.

This module defines the SQLAlchemy model for incomes in the
Finance Tracker application. Incomes represent money received
by users from various sources (e.g., salary, freelance work, investments).
"""

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    TIMESTAMP,
    Float,
    Integer,
    String,
    ForeignKey,
    text,
)
from db.connect import Base


class Income(Base):
    """
    SQLAlchemy model for incomes.
    
    This model represents money received by users from various sources.
    It tracks income transactions and their associated wallets for
    comprehensive financial tracking and analysis.
    
    Attributes:
        id (int): Primary key identifier for the income record
        user_id (str): Foreign key reference to the user who received this income
        wallet_id (str): Foreign key reference to the wallet where income was received
        date (datetime): Date when the income was received (defaults to current time)
        amount (float): The monetary amount of the income
        comment (str, optional): Optional comment or description for the income
        
    Table: incomes
    
    Relationships:
        - user_id -> users.id
        - wallet_id -> wallets.id
    """

    __tablename__ = "incomes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    wallet_id: Mapped[str] = mapped_column(String, ForeignKey("wallets.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    comment: Mapped[str] = mapped_column(String)
