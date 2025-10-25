"""
Transaction categories model for Finance Tracker API.

This module defines the SQLAlchemy model for transaction categories in the
Finance Tracker application. Transaction categories are used to classify
and organize transactions into meaningful groups (e.g., 'Food', 'Transportation',
'Salary', 'Rent') for better financial tracking and analysis.
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from db.connect import Base


class TransactionCategory(Base):
    """
    SQLAlchemy model for transaction categories.

    This model represents categories used to classify and organize
    transactions into meaningful groups. Categories help users
    better understand their spending patterns and financial behavior.

    Attributes:
        id (int): Primary key identifier for the transaction category
        user_id (int): Foreign key reference to the user who owns this category
        name (str): Name of the category (e.g., 'Food', 'Transportation', 'Salary')
        type (str): Type of category (e.g., 'income', 'expense')

    Table: transaction_categories

    Relationships:
        - user_id -> users.id
        - Referenced by Transaction.category_id
    """

    __tablename__ = "transaction_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String)
