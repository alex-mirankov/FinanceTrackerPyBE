"""
Pagination schema module for Finance Tracker API.

This module defines Pydantic models for handling paginated responses
across the Finance Tracker application. It provides a standardized
structure for returning paginated data with metadata about the current
page, total count, and page size.
"""

from pydantic import BaseModel


class Pagination(BaseModel):
    """
    Schema for paginated API responses.
    
    This model provides a standardized structure for paginated responses,
    including the actual content data and pagination metadata.
    
    Attributes:
        content (list): The actual data items for the current page
        totalCount (int): Total number of items across all pages
        page (int): Current page number (1-based indexing)
        size (int): Number of items per page
    """

    content: list
    totalCount: int
    page: int
    size: int
