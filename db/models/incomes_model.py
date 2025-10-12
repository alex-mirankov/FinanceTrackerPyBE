from db.connect import Base
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP, Column, Float, Integer, String, Boolean, ForeignKey, text

class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    wallet_id = Column(String, ForeignKey('wallets.id'), nullable=False)
    date = Column(TIMESTAMP(timezone=True),  nullable=False, server_default=text('now()'))
    amount = Column(Float, nullable=False)
    comment = Column(String)
