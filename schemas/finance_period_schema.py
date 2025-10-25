"""
Finance period schema module for Finance Tracker API.

This module defines Pydantic models for handling finance period data
in the Finance Tracker application. Finance periods represent time
ranges (e.g., monthly, quarterly, yearly) for organizing and tracking
financial data and transactions.
"""

from datetime import datetime
from pydantic import BaseModel


class FinancePeriodCreate(BaseModel):
    """
    Schema for creating a new finance period.
    
    This model defines the required fields for creating a finance period,
    including the time range and descriptive name.
    
    Attributes:
        startDate (datetime): The start date of the finance period
        endDate (datetime): The end date of the finance period
        name (str): A descriptive name for the finance period
    """

    startDate: datetime
    endDate: datetime
    name: str


class FinancePeriodCreateResponse(BaseModel):
    """
    Schema for the response after creating a finance period.
    
    This model represents the data returned after successfully creating
    a finance period, including the generated ID and all period details.
    
    Attributes:
        id (int): The unique identifier of the created finance period
        startDate (datetime): The start date of the finance period
        endDate (datetime): The end date of the finance period
        name (str): A descriptive name for the finance period
    """

    id: int
    startDate: datetime
    endDate: datetime
    name: str


class FinancePeriodResponse(BaseModel):
    """
    Schema for finance period data retrieval.
    
    This model represents a complete finance period object as returned
    from the database, including all period details and metadata.
    
    Attributes:
        id (int): The unique identifier of the finance period
        startDate (datetime): The start date of the finance period
        endDate (datetime): The end date of the finance period
        name (str): A descriptive name for the finance period
    """

    id: int
    startDate: datetime
    endDate: datetime
    name: str

    class Config:
        """
        Pydantic configuration for ORM compatibility.
        
        Enables automatic conversion from SQLAlchemy ORM objects
        to Pydantic models when retrieving data from the database.
        """

        orm_mode = True
