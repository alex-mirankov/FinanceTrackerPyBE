from pydantic import BaseModel

class Pagination(BaseModel):
    content: list
    totalCount: int
    page: int
    size: int