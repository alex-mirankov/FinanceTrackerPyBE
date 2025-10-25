"""
Transaction model for Finance Tracker API.

This module defines the SQLAlchemy model for transactions in the
Finance Tracker application. Transactions represent individual financial
movements (income or expenses) with associated metadata like category,
date, amount, and comments.
"""

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, TIMESTAMP, Float, text, ForeignKey
from db.models.wallets_model import Wallet
from db.connect import Base


class Transaction(Base):
    """
    SQLAlchemy model for financial transactions.
    
    This model represents individual financial movements (income or expenses)
    with associated metadata. It serves as the core entity for tracking
    all financial activities in the application.
    
    Attributes:
        id (int): Primary key identifier for the transaction
        category_id (int): Foreign key reference to the transaction category
        wallet_id (int, optional): Foreign key reference to the wallet involved
        date (datetime): Date when the transaction occurred (defaults to current time)
        amount (float): The monetary amount of the transaction
        comment (str, optional): Optional comment or description for the transaction
        user_id (int): Foreign key reference to the user who owns this transaction
        type (str): Type of transaction (e.g., 'income', 'expense')
        
    Table: transactions
    
    Relationships:
        - category_id -> transaction_categories.id
        - wallet_id -> wallets.id (optional)
        - user_id -> users.id
    """

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("transaction_categories.id"), nullable=False
    )
    wallet_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(Wallet.id), nullable=True
    )
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    type: Mapped[str] = mapped_column(String, nullable=False)
