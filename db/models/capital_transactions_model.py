from db.connect import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, text, ForeignKey

class CapitalTransaction(Base):
    __tablename__ = "capital_transactions"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    currency_id = Column(Integer, ForeignKey('currencies.id'), nullable=False)
    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    capital_storing_place_id = Column(Integer, ForeignKey('capital_storing_places.id'), nullable=False)
    date = Column(TIMESTAMP(timezone=True),  nullable=False, server_default=text('now()'))
    amount = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
