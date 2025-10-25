"""
Wallets model for Finance Tracker API.

This module defines the SQLAlchemy model for wallets in the
Finance Tracker application. Wallets represent virtual containers
where users can organize and track their money across different
accounts or financial instruments.
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from db.connect import Base


class Wallet(Base):
    """
    SQLAlchemy model for wallets.
    
    This model represents virtual containers where users can organize
    and track their money. Wallets help users categorize their
    financial resources and provide better organization for
    financial tracking and analysis.
    
    Attributes:
        id (int): Primary key identifier for the wallet
        user_id (int): Foreign key reference to the user who owns this wallet
        name (str): Name of the wallet (e.g., 'Main Account', 'Savings', 'Investment')
        description (str, optional): Optional description of the wallet's purpose
        
    Table: wallets
    
    Relationships:
        - user_id -> users.id
        - Referenced by Transaction.wallet_id (optional)
        - Referenced by Income.wallet_id
        - Referenced by CapitalTransaction.wallet_id (optional)
    """

    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
