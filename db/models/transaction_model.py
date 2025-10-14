from db.connect import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, text, ForeignKey

from db.models.wallets_model import Wallet

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, nullable=False)
    category_id = Column(Integer, ForeignKey('transaction_categories.id'), nullable=False)
    wallet_id = Column(Integer, ForeignKey(Wallet.id), nullable=True)
    date = Column(TIMESTAMP(timezone=True),  nullable=False, server_default=text('now()'))
    amount = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(String, nullable=False)
