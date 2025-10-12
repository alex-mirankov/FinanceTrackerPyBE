from db.connect import Base
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Column, Float, Integer, String, Boolean, ForeignKey, text

class FinancePeriod(Base):
    __tablename__ = "finance_periods"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    date_start = Column(TIMESTAMP(timezone=True),  nullable=False, server_default=text('now()'))
    date_end = Column(TIMESTAMP(timezone=True),  nullable=False, server_default=text('now()'))
    name = Column(String)
