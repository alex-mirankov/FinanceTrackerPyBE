"""
Capital transactions model for Finance Tracker API.

This module defines the SQLAlchemy model for capital transactions in the
Finance Tracker application. Capital transactions represent movements of
capital between different storing places, currencies, and wallets.
"""

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, TIMESTAMP, Float, text, ForeignKey
from db.connect import Base


class CapitalTransaction(Base):
    """
    SQLAlchemy model for capital transactions.

    This model represents capital movements between different storing places,
    currencies, and wallets. It tracks the flow of capital within the user's
    financial ecosystem.

    Attributes:
        id (int): Primary key identifier for the capital transaction
        user_id (int): Foreign key reference to the user who owns this transaction
        currency_id (int): Foreign key reference to the currency used in this transaction
        wallet_id (int, optional): Foreign key reference to the wallet involved (if applicable)
        capital_storing_place_id (int): Foreign key reference to the capital storing place
        date (datetime): Timestamp when the transaction occurred (defaults to current time)
        amount (float): The monetary amount of the capital transaction
        comment (str, optional): Optional comment or description for the transaction

    Table: capital_transactions

    Relationships:
        - user_id -> users.id
        - currency_id -> currencies.id
        - wallet_id -> wallets.id (optional)
        - capital_storing_place_id -> capital_storing_places.id
    """

    __tablename__ = "capital_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    currency_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("currencies.id"), nullable=False
    )
    wallet_id: Mapped[int] = mapped_column(Integer, ForeignKey("wallets.id"))
    capital_storing_place_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("capital_storing_places.id"), nullable=False
    )
    date: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    comment: Mapped[str] = mapped_column(String, nullable=True)
