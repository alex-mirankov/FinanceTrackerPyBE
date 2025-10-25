"""
Finance periods model for Finance Tracker API.

This module defines the SQLAlchemy model for finance periods in the
Finance Tracker application. Finance periods represent time ranges
(e.g., monthly, quarterly, yearly) for organizing and tracking
financial data and transactions.
"""

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    TIMESTAMP,
    Integer,
    String,
    ForeignKey,
    text,
)
from db.connect import Base


class FinancePeriod(Base):
    """
    SQLAlchemy model for finance periods.

    This model represents time ranges used to organize and track
    financial data. Finance periods help users categorize their
    financial activities into meaningful time segments for better
    analysis and reporting.

    Attributes:
        id (int): Primary key identifier for the finance period
        user_id (str): Foreign key reference to the user who owns this period
        date_start (datetime): Start date of the finance period (defaults to current time)
        date_end (datetime): End date of the finance period (defaults to current time)
        name (str): Descriptive name for the finance period (e.g., 'Q1 2024', 'January 2024')

    Table: finance_periods

    Relationships:
        - user_id -> users.id
    """

    __tablename__ = "finance_periods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    date_start: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    date_end: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    name: Mapped[str] = mapped_column(String)
