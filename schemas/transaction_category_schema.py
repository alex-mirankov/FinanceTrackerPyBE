"""
Transaction category schema module for Finance Tracker API.

This module defines Pydantic models for handling transaction category data
in the Finance Tracker application. Transaction categories are used to
classify and organize transactions into meaningful groups (e.g., 'Food',
'Transportation', 'Salary', 'Rent') for better financial tracking and analysis.
"""

from pydantic import BaseModel


class TransactionCategoryCreate(BaseModel):
    """
    Schema for creating a new transaction category.
    
    This model defines the required fields for creating a transaction category,
    including the category name and type classification.
    
    Attributes:
        name (str): The name of the transaction category (e.g., 'Food', 'Transportation')
        type (str): The type of category (e.g., 'income', 'expense')
    """

    name: str
    type: str


class TransactionCategoryResponse(BaseModel):
    """
    Schema for transaction category data retrieval.
    
    This model represents a complete transaction category object as returned
    from the database, including all category details and metadata.
    
    Attributes:
        id (int): The unique identifier of the transaction category
        name (str): The name of the transaction category
        type (str): The type of category (e.g., 'income', 'expense')
    """

    id: int
    name: str
    type: str

    class Config:
        """
        Pydantic configuration for ORM compatibility.
        
        Enables automatic conversion from SQLAlchemy ORM objects
        to Pydantic models when retrieving data from the database.
        """

        orm_mode = True
