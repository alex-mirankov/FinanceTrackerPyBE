"""
Currencies model for Finance Tracker API.

This module defines the SQLAlchemy model for currencies in the
Finance Tracker application. Currencies represent different monetary
units that can be used in financial transactions (e.g., 'USD', 'EUR', 'GBP').
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from db.connect import Base


class Currency(Base):
    """
    SQLAlchemy model for currencies.

    This model represents different monetary units that can be used
    in financial transactions. It provides a standardized way to
    handle multi-currency support in the application.

    Attributes:
        id (int): Primary key identifier for the currency
        name (str): Name or code of the currency (e.g., 'USD', 'EUR', 'GBP')

    Table: currencies

    Relationships:
        - Referenced by CapitalTransaction.currency_id
    """

    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
