"""
Transaction schema module for Finance Tracker API.

This module defines Pydantic models for handling transaction data
in the Finance Tracker application. Transactions represent individual
financial movements (income or expenses) with associated metadata
like category, date, amount, and comments.
"""

from datetime import datetime
from pydantic import BaseModel


class TransactionCreate(BaseModel):
    """
    Schema for creating a new transaction.

    This model defines the required fields for creating a transaction,
    including financial details and categorization.

    Attributes:
        categoryId (int): The ID of the transaction category
        date (datetime): The date when the transaction occurred
        amount (float): The monetary amount of the transaction
        comment (str): Optional comment or description for the transaction
        type (str): The type of transaction (e.g., 'income', 'expense')
    """

    categoryId: int
    date: datetime
    amount: float
    comment: str
    type: str


class TransactionCreateResponse(BaseModel):
    """
    Schema for the response after creating a transaction.

    This model represents the data returned after successfully creating
    a transaction, including the generated ID and all transaction details.

    Attributes:
        id (int): The unique identifier of the created transaction
        category_id (int): The ID of the transaction category
        date (datetime): The date when the transaction occurred
        amount (float): The monetary amount of the transaction
        comment (str): Optional comment or description for the transaction
        type (str): The type of transaction (e.g., 'income', 'expense')
    """

    id: int
    category_id: int
    date: datetime
    amount: float
    comment: str
    type: str


class TransactionResponse(BaseModel):
    """
    Schema for transaction data retrieval.

    This model represents a complete transaction object as returned
    from the database, including all transaction details and related
    category information.

    Attributes:
        id (int): The unique identifier of the transaction
        category (dict): The complete category object with all details
        date (datetime): The date when the transaction occurred
        amount (float): The monetary amount of the transaction
        comment (str): Optional comment or description for the transaction
        type (str): The type of transaction (e.g., 'income', 'expense')
    """

    id: int
    category: dict
    date: datetime
    amount: float
    comment: str
    type: str

    class Config:
        """
        Pydantic configuration for ORM compatibility.

        Enables automatic conversion from SQLAlchemy ORM objects
        to Pydantic models when retrieving data from the database.
        """

        orm_mode = True
