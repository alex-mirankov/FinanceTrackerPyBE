from db.connect import Base
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    sub_id = Column(String, nullable=False)
    picture = Column(String, nullable=False)
    verified_email = Column(Boolean, server_default="FALSE")
