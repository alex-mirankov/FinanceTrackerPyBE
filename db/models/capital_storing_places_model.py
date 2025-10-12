from db.connect import Base
from sqlalchemy import Column, Integer, String

class CapitalStoringPlace(Base):
    __tablename__ = "capital_storing_places"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
