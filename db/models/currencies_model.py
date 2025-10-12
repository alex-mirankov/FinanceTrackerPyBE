from db.connect import Base
from sqlalchemy import Column, Integer, String

class Currency(Base):
    __tablename__ = "currencies"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
