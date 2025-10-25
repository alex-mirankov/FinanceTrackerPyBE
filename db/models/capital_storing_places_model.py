"""
Capital storing places model for Finance Tracker API.

This module defines the SQLAlchemy model for capital storing places in the
Finance Tracker application. Capital storing places represent physical or
virtual locations where users can store their capital (e.g., 'Bank Account',
'Cash', 'Investment Account', 'Savings Account').
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from db.connect import Base


class CapitalStoringPlace(Base):
    """
    SQLAlchemy model for capital storing places.
    
    This model represents physical or virtual locations where users can
    store their capital. These places are used to categorize and track
    where money is stored or invested.
    
    Attributes:
        id (int): Primary key identifier for the capital storing place
        name (str): Name of the capital storing place (e.g., 'Bank Account', 'Cash')
        
    Table: capital_storing_places
    
    Relationships:
        - Referenced by CapitalTransaction.capital_storing_place_id
    """

    __tablename__ = "capital_storing_places"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
